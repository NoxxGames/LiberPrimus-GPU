"""Runner for Stage 4A full Discord research-bundle generation."""

from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
import zipfile

from libreprimus.discord_full_review import RUN_ID
from libreprimus.discord_full_review.channel_shards import write_channel_shards
from libreprimus.discord_full_review.export import (
    display_path,
    read_json,
    resolve_path,
    write_json,
    write_jsonl,
    write_yaml,
)
from libreprimus.discord_full_review.html_parser import (
    channel_id_for_file,
    channel_name_from_path,
    channel_slug,
    channel_source_record,
    discover_html_files,
    parse_discord_html_file,
)
from libreprimus.discord_full_review.index_extractors import index_records_from_message
from libreprimus.discord_full_review.lp_page_gallery import build_lp_page_gallery
from libreprimus.discord_full_review.models import DEFAULT_OUTPUT_DIR, DEFAULT_PRIVACY_MODE, TOPIC_DEFINITIONS
from libreprimus.discord_full_review.static_site import (
    write_index_page,
    write_site_assets,
    write_site_index,
    write_topic_page,
)
from libreprimus.discord_full_review.topic_classifier import classify_topics


def build_discord_full_review(
    *,
    discord_dir: Path,
    lp_pages_dir: Path,
    out_dir: Path = DEFAULT_OUTPUT_DIR,
    privacy_mode: str = DEFAULT_PRIVACY_MODE,
    include_lp_page_gallery: bool = False,
    allow_warnings: bool = False,
) -> dict[str, Any]:
    if privacy_mode != DEFAULT_PRIVACY_MODE:
        raise ValueError("Only redacted_public privacy mode is supported.")
    resolved_discord = resolve_path(discord_dir)
    resolved_lp_pages = resolve_path(lp_pages_dir)
    resolved_out = resolve_path(out_dir)
    site_dir = resolved_out / "site"
    _ensure_dirs(resolved_out)
    write_site_assets(site_dir)
    generated_at = _utc_now()
    warnings: list[str] = []

    html_files = discover_html_files(resolved_discord)
    if not html_files:
        warnings.append("discord_html_files_missing")

    channel_records: list[dict[str, Any]] = []
    shard_records: list[dict[str, Any]] = []
    topic_records: dict[str, list[dict[str, Any]]] = defaultdict(list)
    indexes: dict[str, list[dict[str, Any]]] = {
        "public_link_index": [],
        "image_reference_index": [],
        "attachment_reference_index": [],
        "method_claim_index": [],
        "numeric_claim_index": [],
        "visual_claim_index": [],
        "debunk_index": [],
    }

    for html_file in html_files:
        channel_name = channel_name_from_path(html_file)
        slug = channel_slug(channel_name)
        channel_id = channel_id_for_file(html_file)
        messages = parse_discord_html_file(html_file, channel_id=channel_id, channel_name=channel_name)
        write_jsonl(resolved_out / "redacted_messages" / f"{slug}.jsonl", messages)
        shard_subset = write_channel_shards(
            out_dir=resolved_out,
            site_dir=site_dir,
            channel_slug=slug,
            channel_name=channel_name,
            channel_id=channel_id,
            messages=messages,
        )
        shard_records.extend(shard_subset)
        channel_records.append(
            channel_source_record(
                html_file,
                source_dir=resolved_discord,
                part_count=len(shard_subset),
                messages=messages,
            )
        )
        for record in messages:
            for topic in classify_topics(record):
                topic_records[topic].append(record)
            record_indexes = index_records_from_message(record)
            indexes["public_link_index"].extend(record_indexes["public_links"])
            indexes["image_reference_index"].extend(record_indexes["image_references"])
            indexes["attachment_reference_index"].extend(record_indexes["attachment_references"])
            indexes["method_claim_index"].extend(record_indexes["method_claims"])
            indexes["numeric_claim_index"].extend(record_indexes["numeric_claims"])
            indexes["visual_claim_index"].extend(record_indexes["visual_claims"])
            indexes["debunk_index"].extend(record_indexes["debunks"])

    topic_shard_count = _write_topic_outputs(resolved_out, site_dir, topic_records)
    _write_index_outputs(resolved_out, site_dir, indexes)
    lp_records = build_lp_page_gallery(lp_pages_dir=resolved_lp_pages, out_dir=resolved_out, site_dir=site_dir) if include_lp_page_gallery else []
    write_jsonl(resolved_out / "lp_pages" / "lp_page_image_manifest.jsonl", lp_records)
    write_jsonl(resolved_out / "lp_pages" / "lp_page_thumbnail_manifest.jsonl", _thumbnail_records(lp_records))

    summary = _build_summary(
        generated_at=generated_at,
        discord_dir=resolved_discord,
        lp_pages_dir=resolved_lp_pages,
        out_dir=resolved_out,
        channel_records=channel_records,
        shard_records=shard_records,
        topic_shard_count=topic_shard_count,
        indexes=indexes,
        lp_records=lp_records,
        warnings=warnings,
    )
    write_jsonl(resolved_out / "warnings.jsonl", [{"warning": warning} for warning in warnings])
    write_jsonl(resolved_out / "channel_records.jsonl", channel_records)
    write_jsonl(resolved_out / "shard_records.jsonl", shard_records)
    write_json(resolved_out / "channel_index.json", {"channels": channel_records})
    _write_channel_index_md(resolved_out / "channel_index.md", channel_records)
    write_json(resolved_out / "summary.json", summary)
    _write_deep_research_manifest(resolved_out / "deep_research_bundle_manifest.yaml", summary, channel_records)
    _write_deep_research_readme(resolved_out / "README_FOR_DEEP_RESEARCH.md", summary)
    _write_sftp_instructions(resolved_out / "SFTP_UPLOAD_INSTRUCTIONS.md")
    write_site_index(site_dir=site_dir, summary=summary, channel_records=channel_records)
    _zip_site(site_dir, resolved_out / "liberprimus-discord-review-site.zip")
    if warnings and not allow_warnings:
        raise RuntimeError("; ".join(warnings))
    return summary


def _ensure_dirs(out_dir: Path) -> None:
    for relative in (
        "site/channels",
        "site/topics",
        "site/indexes",
        "site/lp-pages",
        "site/assets",
        "redacted_messages",
        "channel_shards",
        "topic_shards",
        "indexes",
        "lp_pages",
    ):
        (out_dir / relative).mkdir(parents=True, exist_ok=True)


def _write_topic_outputs(out_dir: Path, site_dir: Path, topic_records: dict[str, list[dict[str, Any]]]) -> int:
    for topic in TOPIC_DEFINITIONS:
        records = topic_records.get(topic, [])
        lines = [f"# {topic}", "", "Generated topic view over the redacted chronological layer.", ""]
        for record in records:
            lines.append(f"- `{record.get('message_ref')}` {record.get('redacted_text', '')}")
        (out_dir / "topic_shards" / f"{topic}.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        write_topic_page(site_dir / "topics" / f"{topic}.html", topic, records)
    return len(TOPIC_DEFINITIONS)


def _write_index_outputs(out_dir: Path, site_dir: Path, indexes: dict[str, list[dict[str, Any]]]) -> None:
    mapping = {
        "public_link_index": "public-links",
        "image_reference_index": "image-references",
        "attachment_reference_index": "attachment-references",
        "method_claim_index": "method-claims",
        "numeric_claim_index": "numeric-claims",
        "visual_claim_index": "visual-claims",
        "debunk_index": "debunks",
    }
    for json_name, page_name in mapping.items():
        records = indexes[json_name]
        write_jsonl(out_dir / "indexes" / f"{json_name}.jsonl", records)
        write_index_page(site_dir / "indexes" / f"{page_name}.html", page_name, records)


def _thumbnail_records(lp_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "record_type": "lp_page_thumbnail_record",
            "image_id": record["image_id"],
            "thumbnail_relative_path": record["thumbnail_relative_path"],
            "raw_source_committed": False,
            "generated_copy_committed": False,
            "solve_claim": False,
        }
        for record in lp_records
    ]


def _build_summary(
    *,
    generated_at: str,
    discord_dir: Path,
    lp_pages_dir: Path,
    out_dir: Path,
    channel_records: list[dict[str, Any]],
    shard_records: list[dict[str, Any]],
    topic_shard_count: int,
    indexes: dict[str, list[dict[str, Any]]],
    lp_records: list[dict[str, Any]],
    warnings: list[str],
) -> dict[str, Any]:
    largest = max(channel_records, key=lambda record: int(record.get("file_size_bytes", 0)), default={})
    return {
        "record_type": "discord_full_review_summary",
        "run_id": RUN_ID,
        "generated_at_utc": generated_at,
        "privacy_mode": DEFAULT_PRIVACY_MODE,
        "discord_source_dir": display_path(discord_dir),
        "lp_pages_source_dir": display_path(lp_pages_dir),
        "discord_html_file_count": len(channel_records),
        "total_bytes_processed": sum(int(record.get("file_size_bytes", 0)) for record in channel_records),
        "channel_count": len(channel_records),
        "largest_channel_name": largest.get("channel_name"),
        "largest_channel_part_count": largest.get("part_count", 0),
        "redacted_message_count": sum(int(record.get("estimated_message_count", 0)) for record in channel_records),
        "channel_shard_count": len(shard_records),
        "topic_shard_count": topic_shard_count,
        "public_link_count": len(indexes["public_link_index"]),
        "image_reference_count": len(indexes["image_reference_index"]),
        "attachment_reference_count": len(indexes["attachment_reference_index"]),
        "method_claim_count": len(indexes["method_claim_index"]),
        "numeric_claim_count": len(indexes["numeric_claim_index"]),
        "visual_claim_count": len(indexes["visual_claim_index"]),
        "debunk_count": len(indexes["debunk_index"]),
        "lp_page_image_count": len(lp_records),
        "lp_page_thumbnail_count": len(lp_records),
        "output_paths": {
            "site_index": display_path(out_dir / "site" / "index.html"),
            "sftp_root": display_path(out_dir / "site"),
            "deep_research_manifest": display_path(out_dir / "deep_research_bundle_manifest.yaml"),
            "channel_index": display_path(out_dir / "channel_index.md"),
            "summary": display_path(out_dir / "summary.json"),
            "zip": display_path(out_dir / "liberprimus-discord-review-site.zip"),
        },
        "warnings": warnings,
        "raw_message_committed": False,
        "username_committed": False,
        "user_id_committed": False,
        "message_id_committed": False,
        "private_url_committed": False,
        "raw_discord_html_committed": False,
        "generated_site_committed": False,
        "raw_lp_page_images_committed": False,
        "solve_claim": False,
        "cuda_used": False,
    }


def _write_channel_index_md(path: Path, channel_records: list[dict[str, Any]]) -> None:
    lines = ["# Stage 4A Channel Index", "", "Redacted full-review channels.", ""]
    for record in channel_records:
        lines.append(
            f"- {record['channel_name']}: {record['estimated_message_count']} messages, "
            f"{record['part_count']} parts, site `{record['site_index_relative_path']}`"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def _write_deep_research_manifest(path: Path, summary: dict[str, Any], channel_records: list[dict[str, Any]]) -> None:
    payload = {
        "manifest_id": "stage4a-deep-research-bundle",
        "purpose": "Deep Research review of redacted Discord archive and LP page gallery.",
        "privacy_mode": DEFAULT_PRIVACY_MODE,
        "site_index": summary["output_paths"]["site_index"],
        "channel_index": summary["output_paths"]["channel_index"],
        "lp_page_gallery": "site/lp-pages/index.html",
        "recommended_first_pass": [
            "topics/source-links-tools-datasets.html",
            "topics/cuneiform-base60.html",
            "topics/page-art-dots-binary-braille-stars.html",
            "indexes/image-references.html",
            "indexes/method-claims.html",
        ],
        "channels": [
            {
                "channel_name": record["channel_name"],
                "part_count": record["part_count"],
                "site_index": record["site_index_relative_path"],
            }
            for record in channel_records
        ],
        "privacy_notes": [
            "Raw Discord logs are not included.",
            "Usernames, user IDs, message IDs, avatar URLs, and private Discord CDN query strings are redacted.",
            "Use generated review views, not raw local third_party directories.",
        ],
        "limitations": [
            "Topic classification is keyword-based and may duplicate messages across views.",
            "Non-empty image or attachment references are review aids, not solve evidence.",
        ],
    }
    write_yaml(path, payload)


def _write_deep_research_readme(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Stage 4A Deep Research Bundle

Open `site/index.html` first. The bundle is redacted public review material generated from local Discord HTML exports.

- Channels: {summary.get('channel_count')}
- Redacted messages: {summary.get('redacted_message_count')}
- Topic shards: {summary.get('topic_shard_count')}
- LP page gallery images: {summary.get('lp_page_image_count')}

Do not use raw Discord logs or raw page images. No solve claim is made.
"""
    path.write_text(text, encoding="utf-8", newline="\n")


def _write_sftp_instructions(path: Path) -> None:
    text = """# SFTP Upload Instructions

Upload the contents of `experiments/results/discord-full-review/stage4a/site/` to the target static web directory.

Do not upload `third_party/LiberPrimusDiscordChats/`, `third_party/LiberPrimusPages/`, or any raw local source directory. Consider `noindex` headers, `robots.txt`, or basic authentication for externally hosted review copies.
"""
    path.write_text(text, encoding="utf-8", newline="\n")


def _zip_site(site_dir: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(site_dir.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(site_dir.parent))


def load_generated_summary(results_dir: Path) -> dict[str, Any]:
    return read_json(resolve_path(results_dir) / "summary.json")


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
