"""Source manifest loading and validation."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from .export import read_yaml, write_json
from .models import (
    MANIFEST_VALIDATION_REPORT,
    OUTPUT_DIR,
    PRIORITIES,
    REQUIRED_SOURCE_IDS,
    SOURCE_TIERS,
    SOURCE_TYPES,
)


def load_manifest(path: Path) -> dict[str, Any]:
    """Load a source manifest document."""

    payload = read_yaml(path)
    if not isinstance(payload, dict):
        raise ValueError(f"source manifest is not a mapping: {path}")
    if not isinstance(payload.get("records"), list):
        raise ValueError(f"source manifest has no records list: {path}")
    return payload


def manifest_records(path: Path) -> list[dict[str, Any]]:
    """Return source records from a manifest."""

    return [dict(record) for record in load_manifest(path)["records"] if isinstance(record, dict)]


def validate_manifest(path: Path, *, out_dir: Path = OUTPUT_DIR) -> tuple[dict[str, Any], list[str]]:
    """Validate required Stage 5AF source-manifest properties."""

    errors: list[str] = []
    warnings: list[str] = []
    try:
        payload = load_manifest(path)
        records = [dict(record) for record in payload["records"] if isinstance(record, dict)]
    except (OSError, ValueError) as exc:
        records = []
        payload = {}
        errors.append(f"manifest_load_failed: {exc}")

    source_ids = [str(record.get("source_id", "")) for record in records]
    duplicate_ids = sorted(source_id for source_id, count in Counter(source_ids).items() if count > 1)
    missing_required = sorted(REQUIRED_SOURCE_IDS.difference(source_ids))
    if duplicate_ids:
        errors.append(f"duplicate_source_ids: {duplicate_ids}")
    if missing_required:
        errors.append(f"missing_required_source_ids: {missing_required}")

    for index, record in enumerate(records):
        _validate_record(errors, warnings, index, record)

    one_hop = payload.get("one_hop_same_domain_links", {})
    if one_hop.get("enabled_by_default") is not False:
        errors.append("one_hop_same_domain_links_must_be_disabled_by_default")

    storage_policy = payload.get("storage_policy", {})
    if storage_policy.get("local_storage_only") is not True:
        errors.append("storage_policy_local_storage_only_not_true")
    if storage_policy.get("google_drive_storage_allowed") is not False:
        errors.append("google_drive_storage_allowed_must_be_false")

    priority_counts = dict(sorted(Counter(record.get("priority", "unknown") for record in records).items()))
    source_type_counts = dict(sorted(Counter(record.get("source_type", "unknown") for record in records).items()))
    summary = {
        "record_type": "source_manifest_validation",
        "source_manifest_records": len(records),
        "required_source_ids_present": not missing_required,
        "duplicate_source_ids": duplicate_ids,
        "missing_required_source_ids": missing_required,
        "priority_counts": priority_counts,
        "source_type_counts": source_type_counts,
        "manual_collection_required_count": sum(
            1 for record in records if record.get("manual_collection_required") is True
        ),
        "network_default_allowed": False,
        "local_storage_only": storage_policy.get("local_storage_only") is True,
        "google_drive_storage_allowed": storage_policy.get("google_drive_storage_allowed"),
        "validation_error_count": len(errors),
        "validation_warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
    }
    write_json(out_dir / MANIFEST_VALIDATION_REPORT, summary)
    return summary, errors


def _validate_record(
    errors: list[str],
    warnings: list[str],
    index: int,
    record: dict[str, Any],
) -> None:
    source_id = record.get("source_id", f"index-{index}")
    for field in (
        "source_id",
        "title",
        "source_type",
        "priority",
        "source_tier",
        "collection_status",
        "recommended_capture_modes",
        "manual_collection_required",
        "allow_network_fetch",
        "allow_dynamic_browser",
        "expected_outputs",
        "known_limitations",
        "what_it_supports",
        "what_it_does_not_support",
        "related_leads",
        "notes",
    ):
        if field not in record:
            errors.append(f"{source_id}: missing_field:{field}")
    if record.get("priority") not in PRIORITIES:
        errors.append(f"{source_id}: invalid_priority:{record.get('priority')}")
    if record.get("source_type") not in SOURCE_TYPES:
        errors.append(f"{source_id}: invalid_source_type:{record.get('source_type')}")
    if record.get("source_tier") not in SOURCE_TIERS:
        errors.append(f"{source_id}: invalid_source_tier:{record.get('source_tier')}")
    if record.get("solve_claim") is not False:
        errors.append(f"{source_id}: solve_claim_must_be_false")
    if record.get("raw_commit_allowed") is not False:
        errors.append(f"{source_id}: raw_commit_allowed_must_be_false")
    if record.get("google_drive_storage_allowed") is not False:
        errors.append(f"{source_id}: google_drive_storage_allowed_must_be_false")
    if record.get("source_type") in {"google_sheet", "google_doc", "google_colab"}:
        if record.get("manual_collection_required") is not True:
            errors.append(f"{source_id}: google_sources_must_be_manual_export")
        limitations = " ".join(str(item).lower() for item in record.get("known_limitations", []))
        if "local" not in limitations or "google drive" not in limitations:
            warnings.append(f"{source_id}: google_manual_export_note_should_mention_local_storage")
