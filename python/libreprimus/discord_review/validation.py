"""Validation for Stage 3Q Discord review bundles and aggregate records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.discord_review.export import read_json, read_yaml
from libreprimus.paths import repo_root

FORBIDDEN_TEXT_MARKERS = (
    "username:",
    "user_id:",
    "message_id:",
    "avatar_url:",
    "cdn.discordapp.com/attachments/",
    "media.discordapp.net/attachments/",
    "raw_message:",
    "message_body:",
)


def validate_bundles(
    *,
    results_dir: Path,
    aggregate: Path,
    allow_missing: bool = False,
) -> tuple[dict[str, int], list[str]]:
    resolved_results = _resolve(results_dir)
    resolved_aggregate = _resolve(aggregate)
    errors: list[str] = []
    counts = {
        "topic_shard_count": 0,
        "review_lead_count": 0,
        "redacted_message_count": 0,
    }
    if not resolved_results.is_dir():
        if allow_missing:
            _validate_aggregate_if_present(resolved_aggregate, errors)
            return counts, errors
        errors.append(f"missing results dir: {resolved_results}")
        return counts, errors
    summary_path = resolved_results / "review_bundle_summary.json"
    if not summary_path.is_file():
        if allow_missing:
            _validate_aggregate_if_present(resolved_aggregate, errors)
            return counts, errors
        errors.append(f"missing summary: {summary_path}")
        return counts, errors
    summary = read_json(summary_path)
    counts["topic_shard_count"] = int(summary.get("topic_shard_count", 0))
    counts["review_lead_count"] = int(summary.get("review_lead_count", 0))
    counts["redacted_message_count"] = int(summary.get("redacted_message_count", 0))
    _validate_privacy_flags(summary, errors, "summary")
    for required in [
        "redacted_message_stream.jsonl",
        "source_links_index.jsonl",
        "method_claims_index.jsonl",
        "numeric_observations_index.jsonl",
        "visual_observations_index.jsonl",
        "debunks_and_false_positives_index.jsonl",
        "attachment_reference_index.jsonl",
        "review_index.html",
    ]:
        if not (resolved_results / required).is_file():
            errors.append(f"missing generated output: {required}")
    if not (resolved_results / "topic_shards").is_dir():
        errors.append("missing topic_shards directory")
    _validate_aggregate_if_present(resolved_aggregate, errors)
    return counts, errors


def _validate_aggregate_if_present(path: Path, errors: list[str]) -> None:
    if not path.is_file():
        return
    payload = read_yaml(path)
    _validate_privacy_flags(payload, errors, "aggregate")
    text = path.read_text(encoding="utf-8").lower()
    for marker in FORBIDDEN_TEXT_MARKERS:
        if marker in text:
            errors.append(f"aggregate contains forbidden marker: {marker}")


def _validate_privacy_flags(payload: dict[str, Any], errors: list[str], label: str) -> None:
    false_fields = [
        "raw_logs_committed",
        "raw_message_committed",
        "username_committed",
        "private_url_committed",
        "ai_upload_used",
        "live_api_used",
        "scrape_used",
        "solve_claim",
    ]
    for field in false_fields:
        if field in payload and payload[field] is not False:
            errors.append(f"{label}: {field} must be false")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path
