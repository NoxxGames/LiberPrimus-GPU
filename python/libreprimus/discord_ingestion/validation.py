"""Validation helpers for Stage 3N Discord ingestion records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.discord_ingestion.export import read_json, read_jsonl, read_yaml
from libreprimus.paths import repo_root

RESULT_FILES = {
    "file_locks": "discord_html_file_locks.jsonl",
    "links": "discord_extracted_links.jsonl",
    "attachments": "discord_attachment_candidates.jsonl",
    "method_claims": "discord_method_claim_candidates.jsonl",
    "numeric": "discord_numeric_observation_candidates.jsonl",
    "summary": "discord_ingestion_summary.json",
}

SCHEMA_FILES = {
    "archive": repo_root() / "schemas/history/discord-archive-record-v0.schema.json",
    "file_locks": repo_root() / "schemas/history/discord-html-file-lock-v0.schema.json",
    "links": repo_root() / "schemas/history/discord-extracted-link-v0.schema.json",
    "attachments": repo_root() / "schemas/history/discord-attachment-candidate-v0.schema.json",
    "method_claims": repo_root() / "schemas/history/discord-method-claim-candidate-v0.schema.json",
    "numeric": repo_root()
    / "schemas/history/discord-numeric-observation-candidate-v0.schema.json",
    "summary": repo_root() / "schemas/history/discord-ingestion-summary-v0.schema.json",
}

FORBIDDEN_AGGREGATE_MARKERS = (
    "message_body:",
    "raw_message:",
    "username:",
    "user_id:",
    "avatar:",
    "cdn.discordapp.com/attachments",
    "media.discordapp.net/attachments",
)


def validate_results(results_dir: Path, *, allow_missing: bool = False) -> tuple[dict[str, int], list[str]]:
    """Validate generated Discord ingestion records when present."""
    resolved = _resolve(results_dir)
    if not resolved.exists():
        if allow_missing:
            return {"html_file_count": 0}, []
        return {"html_file_count": 0}, [f"results directory missing: {resolved}"]
    if allow_missing and not (resolved / "discord_ingestion_summary.json").is_file():
        return {"html_file_count": 0}, []

    errors: list[str] = []
    counts: dict[str, int] = {}
    for key, filename in RESULT_FILES.items():
        path = resolved / filename
        if key == "summary":
            if not path.is_file():
                errors.append(f"missing summary: {path}")
                continue
            payload = read_json(path)
            _validate_schema(key, payload, errors)
            _validate_privacy_flags(payload, errors)
            counts["html_file_count"] = int(payload.get("html_file_count", 0))
            counts["link_count"] = int(payload.get("link_count", 0))
            counts["method_claim_candidate_count"] = int(
                payload.get("method_claim_candidate_count", 0)
            )
            counts["numeric_observation_candidate_count"] = int(
                payload.get("numeric_observation_candidate_count", 0)
            )
            continue
        if not path.is_file():
            errors.append(f"missing records: {path}")
            continue
        records = read_jsonl(path)
        counts[f"{key}_record_count"] = len(records)
        for record in records:
            _validate_schema(key, record, errors)
            _validate_privacy_flags(record, errors)
            _validate_record_specific_rules(key, record, errors)
    return counts, errors


def export_aggregate_records(
    *,
    results_dir: Path,
    archive_out: Path,
    observation_out: Path,
    allow_missing: bool = False,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Write committed aggregate records from generated scan summary."""
    from libreprimus.discord_ingestion.export import write_yaml
    from libreprimus.discord_ingestion.models import ARCHIVE_ID, SOURCE_STATUS

    resolved_results = _resolve(results_dir)
    if not (resolved_results / "discord_ingestion_summary.json").is_file():
        if allow_missing:
            summary = _empty_summary()
        else:
            raise FileNotFoundError(resolved_results / "discord_ingestion_summary.json")
    else:
        summary = read_json(resolved_results / "discord_ingestion_summary.json")

    archive_record = {
        "record_type": "discord_archive_record",
        "archive_id": ARCHIVE_ID,
        "description": (
            "Admin-provided local Discord HTML export; committed record contains aggregate "
            "source-lock metadata only."
        ),
        "source_status": SOURCE_STATUS,
        "raw_logs_committed": False,
        "message_bodies_committed": False,
        "usernames_committed": False,
        "ai_upload_allowed": False,
        "live_api_used": False,
        "scrape_used": False,
        "local_path": "third_party/LiberPrimusDiscordChats",
        "created_at_utc": str(summary.get("generated_at_utc", "")),
        "notes": "Raw Discord logs remain local and ignored; Discord claims are review leads only.",
    }
    observation_record = {
        key: value
        for key, value in summary.items()
        if key
        in {
            "record_type",
            "archive_id",
            "generated_at_utc",
            "html_file_count",
            "total_bytes",
            "link_count",
            "unique_domain_count",
            "attachment_candidate_count",
            "method_claim_candidate_count",
            "numeric_observation_candidate_count",
            "warning_count",
            "raw_logs_committed",
            "message_bodies_committed",
            "usernames_committed",
            "ai_upload_used",
            "live_api_used",
            "scrape_used",
            "output_paths",
            "notes",
        }
    }
    observation_record["notes"] = (
        "Aggregate Stage 3N summary only; generated review records remain ignored."
    )
    write_yaml(_resolve(archive_out), archive_record)
    write_yaml(_resolve(observation_out), observation_record)
    errors = validate_aggregate_records(
        archive_record_path=archive_out,
        observation_record_path=observation_out,
        allow_missing=False,
    )[1]
    if errors:
        raise ValueError("; ".join(errors))
    return archive_record, observation_record


def validate_aggregate_records(
    *,
    archive_record_path: Path,
    observation_record_path: Path,
    allow_missing: bool = False,
) -> tuple[dict[str, int], list[str]]:
    """Validate committed aggregate records."""
    archive_path = _resolve(archive_record_path)
    observation_path = _resolve(observation_record_path)
    if allow_missing and (not archive_path.is_file() or not observation_path.is_file()):
        return {"aggregate_record_count": 0}, []
    errors: list[str] = []
    archive = read_yaml(archive_path)
    observation = read_yaml(observation_path)
    _validate_schema("archive", archive, errors)
    _validate_schema("summary", observation, errors)
    for record in (archive, observation):
        _validate_privacy_flags(record, errors)
    for path in (archive_path, observation_path):
        text = path.read_text(encoding="utf-8").lower()
        for marker in FORBIDDEN_AGGREGATE_MARKERS:
            if marker in text:
                errors.append(f"{path}: forbidden committed aggregate marker {marker}")
    return {"aggregate_record_count": 2}, errors


def _empty_summary() -> dict[str, Any]:
    return {
        "record_type": "discord_ingestion_summary",
        "archive_id": "admin-provided-discord-html-stage3n",
        "generated_at_utc": "",
        "html_file_count": 0,
        "total_bytes": 0,
        "link_count": 0,
        "unique_domain_count": 0,
        "attachment_candidate_count": 0,
        "method_claim_candidate_count": 0,
        "numeric_observation_candidate_count": 0,
        "warning_count": 0,
        "raw_logs_committed": False,
        "message_bodies_committed": False,
        "usernames_committed": False,
        "ai_upload_used": False,
        "live_api_used": False,
        "scrape_used": False,
        "output_paths": {},
        "notes": "No local Discord scan results were present when aggregate was exported.",
    }


def _validate_schema(key: str, record: dict[str, Any], errors: list[str]) -> None:
    schema = json.loads(SCHEMA_FILES[key].read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    for error in validator.iter_errors(record):
        errors.append(f"{key}: {error.message}")


def _validate_privacy_flags(record: dict[str, Any], errors: list[str]) -> None:
    record_id = (
        record.get("archive_id")
        or record.get("link_id")
        or record.get("attachment_id")
        or record.get("claim_id")
        or record.get("observation_id")
        or "<unknown>"
    )
    expected_false = {
        "raw_logs_committed",
        "message_bodies_committed",
        "usernames_committed",
        "ai_upload_allowed",
        "ai_upload_used",
        "live_api_used",
        "scrape_used",
        "raw_content_committed",
        "message_body_committed",
        "raw_message_committed",
    }
    for key in expected_false:
        if key in record and record.get(key) is not False:
            errors.append(f"{record_id}: {key} must be false")


def _validate_record_specific_rules(key: str, record: dict[str, Any], errors: list[str]) -> None:
    record_id = (
        record.get("link_id")
        or record.get("attachment_id")
        or record.get("claim_id")
        or record.get("observation_id")
        or "<unknown>"
    )
    if key == "links" and record.get("surrounding_text_redacted") is not True:
        errors.append(f"{record_id}: link surrounding text must be redacted")
    if key == "attachments" and record.get("private_url_redacted") is not True:
        errors.append(f"{record_id}: attachment private URL must be redacted")
    url_fields = [
        str(record.get("url", "")),
        str(record.get("normalized_url", "")),
        str(record.get("url_or_path_redacted", "")),
    ]
    for value in url_fields:
        if "discord" in value.lower() and ("?" in value or "&" in value):
            errors.append(f"{record_id}: Discord URL query string must be redacted")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path
