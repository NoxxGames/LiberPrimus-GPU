"""Validation for Stage 4A full-review generated outputs and aggregates."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.discord_full_review.export import read_json, read_jsonl, resolve_path
from libreprimus.discord_full_review.redaction import has_private_discord_url


def validate_results(results_dir: Path, *, allow_missing: bool = False) -> tuple[dict[str, Any], list[str]]:
    resolved = resolve_path(results_dir)
    if not resolved.is_dir():
        if allow_missing:
            return {"results_present": False}, []
        return {}, [f"results_dir_missing: {resolved}"]
    errors: list[str] = []
    required = [
        resolved / "site" / "index.html",
        resolved / "site" / "robots.txt",
        resolved / "site" / "SITE_PRIVACY_NOTICE.md",
        resolved / "site" / "SFTP_UPLOAD_CHECKLIST.md",
        resolved / "site" / ".htaccess.example",
        resolved / "site" / "site_manifest.json",
        resolved / "site" / "site_manifest.md",
        resolved / "channel_index.md",
        resolved / "channel_index.json",
        resolved / "deep_research_bundle_manifest.yaml",
        resolved / "summary.json",
        resolved / "indexes" / "public_link_index.jsonl",
        resolved / "indexes" / "image_reference_index.jsonl",
        resolved / "indexes" / "attachment_reference_index.jsonl",
        resolved / "lp_pages" / "lp_page_image_manifest.jsonl",
    ]
    for path in required:
        if not path.is_file():
            errors.append(f"required_output_missing: {path}")
    _validate_noindex_html(resolved, errors)
    _validate_privacy_files(resolved, errors)
    _validate_site_manifest(resolved, errors)
    summary: dict[str, Any] = {}
    if (resolved / "summary.json").is_file():
        summary = read_json(resolved / "summary.json")
        for key in (
            "raw_message_committed",
            "username_committed",
            "user_id_committed",
            "message_id_committed",
            "private_url_committed",
            "raw_discord_html_committed",
            "generated_site_committed",
            "solve_claim",
        ):
            if summary.get(key) is not False:
                errors.append(f"summary_{key}_must_be_false")
    for stream in (resolved / "redacted_messages").glob("*.jsonl"):
        for record in read_jsonl(stream):
            text = str(record.get("redacted_text", ""))
            if has_private_discord_url(text):
                errors.append(f"private_discord_url_in_redacted_text: {stream}")
                break
            for key in ("raw_message_committed", "username_committed", "user_id_committed", "message_id_committed", "private_url_committed"):
                if record.get(key) is not False:
                    errors.append(f"{stream}:{record.get('message_ref')} {key}_must_be_false")
                    break
    return summary, errors


def _validate_noindex_html(results_dir: Path, errors: list[str]) -> None:
    meta = '<meta name="robots" content="noindex,nofollow,noarchive">'
    samples = [results_dir / "site" / "index.html"]
    samples.extend(sorted((results_dir / "site" / "channels").glob("*/*.html"))[:3])
    samples.extend(sorted((results_dir / "site" / "topics").glob("*.html"))[:3])
    samples.extend(sorted((results_dir / "site" / "indexes").glob("*.html"))[:3])
    gallery = results_dir / "site" / "lp-pages" / "index.html"
    if gallery.is_file():
        samples.append(gallery)
    for path in samples:
        if path.is_file() and meta not in path.read_text(encoding="utf-8", errors="ignore"):
            errors.append(f"noindex_meta_missing: {path}")


def _validate_privacy_files(results_dir: Path, errors: list[str]) -> None:
    robots = results_dir / "site" / "robots.txt"
    if robots.is_file():
        text = robots.read_text(encoding="utf-8", errors="ignore")
        if "User-agent: *" not in text or "Disallow: /" not in text:
            errors.append("robots_txt_must_disallow_all")
    notice = results_dir / "site" / "SITE_PRIVACY_NOTICE.md"
    if notice.is_file() and "redacted research review site" not in notice.read_text(encoding="utf-8", errors="ignore").lower():
        errors.append("site_privacy_notice_missing_redacted_context")


def _validate_site_manifest(results_dir: Path, errors: list[str]) -> None:
    manifest_path = results_dir / "site" / "site_manifest.json"
    summary_path = results_dir / "summary.json"
    if not manifest_path.is_file() or not summary_path.is_file():
        return
    manifest = read_json(manifest_path)
    summary = read_json(summary_path)
    if manifest.get("noindex_enabled") is not True:
        errors.append("site_manifest_noindex_enabled_must_be_true")
    if manifest.get("robots_disallow_all") is not True:
        errors.append("site_manifest_robots_disallow_all_must_be_true")
    comparable = {
        "channel_count": "channel_count",
        "channel_part_count": "channel_shard_count",
        "topic_count": "topic_shard_count",
        "public_link_count": "public_link_count",
        "image_reference_count": "image_reference_count",
        "attachment_reference_count": "attachment_reference_count",
        "lp_page_image_count": "lp_page_image_count",
    }
    for manifest_key, summary_key in comparable.items():
        if manifest.get(manifest_key) != summary.get(summary_key):
            errors.append(f"site_manifest_count_mismatch:{manifest_key}")


def validate_aggregate_record(path: Path) -> list[str]:
    text = resolve_path(path).read_text(encoding="utf-8") if resolve_path(path).is_file() else ""
    errors: list[str] = []
    forbidden = ("username", "user_id", "message_id", "cdn.discord", "media.discord")
    for term in forbidden:
        if term in text.lower() and term not in {"username", "user_id", "message_id"}:
            errors.append(f"aggregate_contains_private_term:{term}")
    return errors
