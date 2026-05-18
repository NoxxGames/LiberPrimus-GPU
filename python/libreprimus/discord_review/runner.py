"""Stage 3Q Discord review-bundle runner."""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from libreprimus.discord_review import RUN_ID
from libreprimus.discord_review.export import read_json, write_json, write_jsonl, write_yaml
from libreprimus.discord_review.lead_builder import build_review_leads
from libreprimus.discord_review.redacted_stream import build_redacted_stream
from libreprimus.discord_review.review_index import write_review_index
from libreprimus.discord_review.shard_writer import write_topic_shards
from libreprimus.paths import repo_root


def build_review_bundles(
    *,
    ingestion_dir: Path,
    promotion_dir: Path,
    raw_dir: Path,
    out_dir: Path,
    aggregate_out: Path,
    allow_missing: bool = False,
    allow_warnings: bool = False,
) -> dict[str, Any]:
    """Build redacted, topic-sharded Discord review bundles."""
    resolved_ingestion = _resolve(ingestion_dir)
    resolved_promotion = _resolve(promotion_dir)
    resolved_raw = _resolve(raw_dir)
    resolved_out = _resolve(out_dir)
    resolved_aggregate = _resolve(aggregate_out)
    warnings: list[str] = []

    required_stage3n = [
        resolved_ingestion / "discord_extracted_links.jsonl",
        resolved_ingestion / "discord_method_claim_candidates.jsonl",
        resolved_ingestion / "discord_numeric_observation_candidates.jsonl",
    ]
    has_stage3n = resolved_ingestion.is_dir() and all(path.is_file() for path in required_stage3n)
    if not has_stage3n:
        warnings.append("stage3n_generated_discord_outputs_missing")
        if not allow_missing:
            raise FileNotFoundError(resolved_ingestion)

    generated_at = _utc_now()
    resolved_out.mkdir(parents=True, exist_ok=True)
    (resolved_out / "topic_shards").mkdir(parents=True, exist_ok=True)

    if has_stage3n:
        redacted_stream = build_redacted_stream(resolved_ingestion, generated_at=generated_at)
        review_leads = build_review_leads(ingestion_dir=resolved_ingestion, promotion_dir=resolved_promotion)
    else:
        redacted_stream = []
        review_leads = []

    shard_records = write_topic_shards(out_dir=resolved_out, leads=review_leads, generated_at=generated_at)
    summary = _build_summary(
        generated_at=generated_at,
        ingestion_dir=resolved_ingestion,
        raw_dir=resolved_raw,
        out_dir=resolved_out,
        redacted_stream=redacted_stream,
        review_leads=review_leads,
        shard_records=shard_records,
        warnings=warnings,
    )
    review_index_path = write_review_index(out_dir=resolved_out, shard_records=shard_records, summary=summary)
    summary["output_paths"]["review_index"] = _display_path(review_index_path)

    write_jsonl(resolved_out / "redacted_message_stream.jsonl", redacted_stream)
    write_jsonl(resolved_out / "source_links_index.jsonl", _filter_leads(review_leads, "source_link"))
    write_jsonl(resolved_out / "method_claims_index.jsonl", _filter_leads(review_leads, "method_claim"))
    write_jsonl(resolved_out / "numeric_observations_index.jsonl", _filter_leads(review_leads, "numeric_observation"))
    write_jsonl(resolved_out / "visual_observations_index.jsonl", _visual_leads(review_leads))
    write_jsonl(
        resolved_out / "debunks_and_false_positives_index.jsonl",
        _filter_leads(review_leads, "debunk_or_false_positive"),
    )
    write_jsonl(resolved_out / "attachment_reference_index.jsonl", _attachment_records(redacted_stream))
    write_jsonl(resolved_out / "topic_shard_records.jsonl", shard_records)
    write_jsonl(resolved_out / "warnings.jsonl", [{"warning": warning} for warning in warnings])
    write_json(resolved_out / "review_bundle_summary.json", summary)
    write_yaml(resolved_aggregate, _aggregate(summary))

    if warnings and not allow_warnings:
        raise RuntimeError("; ".join(warnings))
    return summary


def _build_summary(
    *,
    generated_at: str,
    ingestion_dir: Path,
    raw_dir: Path,
    out_dir: Path,
    redacted_stream: list[dict[str, Any]],
    review_leads: list[dict[str, Any]],
    shard_records: list[dict[str, Any]],
    warnings: list[str],
) -> dict[str, Any]:
    ingestion_summary = _read_ingestion_summary(ingestion_dir)
    html_file_count, total_bytes = _raw_counts(raw_dir, ingestion_summary)
    public_links = sorted({link for lead in review_leads for link in lead.get("public_links", [])})
    topic_counts = Counter(str(lead.get("topic", "unknown")) for lead in review_leads)
    method_claim_count = sum(1 for lead in review_leads if lead.get("evidence_type") == "method_claim")
    numeric_count = sum(1 for lead in review_leads if lead.get("evidence_type") == "numeric_observation")
    visual_count = sum(1 for lead in review_leads if _is_visual_lead(lead))
    debunk_count = sum(1 for lead in review_leads if lead.get("evidence_type") == "debunk_or_false_positive")
    return {
        "record_type": "discord_review_bundle_summary",
        "bundle_id": RUN_ID,
        "generated_at_utc": generated_at,
        "html_file_count": html_file_count,
        "total_bytes_scanned": total_bytes,
        "redacted_message_count": len(redacted_stream),
        "topic_shard_count": len(shard_records),
        "review_lead_count": len(review_leads),
        "public_link_count": len(public_links),
        "method_claim_count": method_claim_count,
        "numeric_observation_count": numeric_count,
        "visual_observation_count": visual_count,
        "debunk_count": debunk_count,
        "topic_lead_counts": dict(sorted(topic_counts.items())),
        "topic_names": sorted(topic_counts),
        "output_paths": {
            "redacted_message_stream": _display_path(out_dir / "redacted_message_stream.jsonl"),
            "topic_shards": _display_path(out_dir / "topic_shards"),
            "source_links_index": _display_path(out_dir / "source_links_index.jsonl"),
            "method_claims_index": _display_path(out_dir / "method_claims_index.jsonl"),
            "numeric_observations_index": _display_path(out_dir / "numeric_observations_index.jsonl"),
            "visual_observations_index": _display_path(out_dir / "visual_observations_index.jsonl"),
            "debunks_and_false_positives_index": _display_path(
                out_dir / "debunks_and_false_positives_index.jsonl"
            ),
            "attachment_reference_index": _display_path(out_dir / "attachment_reference_index.jsonl"),
            "summary": _display_path(out_dir / "review_bundle_summary.json"),
            "warnings": _display_path(out_dir / "warnings.jsonl"),
        },
        "warnings": warnings,
        "raw_logs_committed": False,
        "raw_message_committed": False,
        "username_committed": False,
        "private_url_committed": False,
        "ai_upload_used": False,
        "live_api_used": False,
        "scrape_used": False,
        "solve_claim": False,
        "notes": "Generated review bundles are redacted, ignored AI-review aids and not source evidence.",
    }


def _aggregate(summary: dict[str, Any]) -> dict[str, Any]:
    allowed_keys = {
        "record_type",
        "bundle_id",
        "generated_at_utc",
        "html_file_count",
        "total_bytes_scanned",
        "redacted_message_count",
        "topic_shard_count",
        "review_lead_count",
        "public_link_count",
        "method_claim_count",
        "numeric_observation_count",
        "visual_observation_count",
        "debunk_count",
        "topic_lead_counts",
        "topic_names",
        "output_paths",
        "warnings",
        "raw_logs_committed",
        "raw_message_committed",
        "username_committed",
        "private_url_committed",
        "ai_upload_used",
        "live_api_used",
        "scrape_used",
        "solve_claim",
        "notes",
    }
    return {key: summary[key] for key in allowed_keys if key in summary}


def _read_ingestion_summary(ingestion_dir: Path) -> dict[str, Any]:
    path = ingestion_dir / "discord_ingestion_summary.json"
    if path.is_file():
        return read_json(path)
    return {}


def _raw_counts(raw_dir: Path, ingestion_summary: dict[str, Any]) -> tuple[int, int]:
    if ingestion_summary:
        return int(ingestion_summary.get("html_file_count", 0)), int(ingestion_summary.get("total_bytes", 0))
    if not raw_dir.is_dir():
        return 0, 0
    files = [path for path in raw_dir.rglob("*") if path.is_file() and path.suffix.lower() in {".html", ".htm"}]
    return len(files), sum(path.stat().st_size for path in files)


def _filter_leads(leads: list[dict[str, Any]], evidence_type: str) -> list[dict[str, Any]]:
    return [lead for lead in leads if lead.get("evidence_type") == evidence_type]


def _visual_leads(leads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [lead for lead in leads if _is_visual_lead(lead)]


def _is_visual_lead(lead: dict[str, Any]) -> bool:
    topic = str(lead.get("topic", ""))
    return topic in {
        "cuneiform-base60-and-babylonian",
        "page-art-dots-binary-braille-stars",
        "image-artwork-symbols-and-visual-clues",
        "outguess-stego-audio-spectrograms",
        "number-squares-and-onion7",
    }


def _attachment_records(redacted_stream: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for record in redacted_stream:
        for file_name in record.get("attachment_filenames", []):
            records.append(
                {
                    "record_type": "discord_review_attachment_reference",
                    "record_id": record["record_id"],
                    "attachment_filename": file_name,
                    "private_url_committed": False,
                    "raw_message_committed": False,
                    "username_committed": False,
                    "notes": "Attachment reference only; URL is redacted.",
                }
            )
    return records


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root()).as_posix()
    except ValueError:
        return path.as_posix()
