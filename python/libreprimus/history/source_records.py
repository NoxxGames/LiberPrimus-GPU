"""Source archive record loading and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.paths import repo_root

SOURCE_CLASSES = {
    "primary_signed",
    "strong_community_technical",
    "secondary_archive",
    "reference_only_tooling",
    "archived_claim",
    "speculative_observation",
    "negative_control_material",
}
REVIEW_STATUSES = {
    "unreviewed",
    "machine_checked",
    "human_review_required",
    "accepted_as_observation",
    "rejected",
}
CANONICAL_STATUSES = {"noncanonical", "canonical_candidate"}


def resolve_repo_path(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def load_yaml_records(path: Path) -> list[dict[str, Any]]:
    resolved = resolve_repo_path(path)
    payload = yaml.safe_load(resolved.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("records"), list):
        raise ValueError(f"Record file must contain a records list: {resolved}")
    records = payload["records"]
    if not all(isinstance(record, dict) for record in records):
        raise ValueError(f"Every record must be a mapping: {resolved}")
    return records


def validate_source_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {
        "record_type",
        "source_id",
        "title",
        "url",
        "source_class",
        "provenance_notes",
        "retrieval_status",
        "mirror_status",
        "canonical_status",
        "trusted_as_canonical",
        "review_status",
        "notes",
    }
    missing = sorted(required - set(record))
    if missing:
        errors.append(f"{record.get('source_id', '<unknown>')}: missing fields {missing}")
    if record.get("record_type") != "source_archive_record":
        errors.append(f"{record.get('source_id', '<unknown>')}: wrong record_type")
    if record.get("source_class") not in SOURCE_CLASSES:
        errors.append(f"{record.get('source_id', '<unknown>')}: invalid source_class")
    if record.get("review_status") not in REVIEW_STATUSES:
        errors.append(f"{record.get('source_id', '<unknown>')}: invalid review_status")
    if record.get("canonical_status") not in CANONICAL_STATUSES:
        errors.append(f"{record.get('source_id', '<unknown>')}: canonical_status cannot be active")
    if record.get("trusted_as_canonical") is not False:
        errors.append(f"{record.get('source_id', '<unknown>')}: trusted_as_canonical must be false")
    return errors


def validate_source_records(path: Path) -> tuple[int, list[str]]:
    records = load_yaml_records(path)
    errors: list[str] = []
    seen: set[str] = set()
    for record in records:
        source_id = str(record.get("source_id", ""))
        if source_id in seen:
            errors.append(f"{source_id}: duplicate source_id")
        seen.add(source_id)
        errors.extend(validate_source_record(record))
    return len(records), errors
