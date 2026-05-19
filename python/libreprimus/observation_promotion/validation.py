"""Validation for Stage 4L observation promotion records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.observation_promotion.loaders import load_yaml_records
from libreprimus.observation_promotion.models import PROMOTION_CATEGORIES


def validate_observation_promotion_records(
    *,
    ledger: Path,
    readiness: Path,
    blockers: Path,
    manifest_readiness: Path,
    summary: Path,
) -> tuple[dict[str, int], list[str]]:
    """Validate committed Stage 4L records."""

    ledger_records = load_yaml_records(ledger)
    readiness_records = load_yaml_records(readiness)
    blocker_records = load_yaml_records(blockers)
    manifest_records = load_yaml_records(manifest_readiness)
    summary_records = load_yaml_records(summary)
    errors: list[str] = []
    counts = {
        "ledger_records": len(ledger_records),
        "readiness_records": len(readiness_records),
        "blocker_records": len(blocker_records),
        "manifest_readiness_records": len(manifest_records),
        "summary_records": len(summary_records),
    }
    if not ledger_records:
        errors.append("ledger_records_missing")
    if len(ledger_records) != len(readiness_records):
        errors.append("ledger_readiness_count_mismatch")
    if len(summary_records) != 1:
        errors.append("summary_record_missing")
    blocker_ids = {str(record.get("blocker_record_id")) for record in blocker_records}
    for record in [*ledger_records, *readiness_records]:
        _validate_promotion_record(record, blocker_ids, errors)
    for record in blocker_records:
        _validate_common_flags(record, errors)
        if not record.get("reason"):
            errors.append(f"blocker_reason_missing:{record.get('blocker_record_id')}")
    for record in manifest_records:
        _validate_common_flags(record, errors)
        if record.get("execution_enabled") is not False:
            errors.append(f"manifest_execution_enabled:{record.get('manifest_readiness_id')}")
        if record.get("ready_state") in {"blocked", "deferred"} and not record.get("blockers"):
            errors.append(f"manifest_blockers_missing:{record.get('manifest_readiness_id')}")
    if summary_records:
        summary_record = summary_records[0]
        _validate_common_flags(summary_record, errors)
        if int(summary_record.get("ledger_records_created") or -1) != len(ledger_records):
            errors.append("summary_ledger_count_mismatch")
        if int(summary_record.get("manifest_readiness_records_created") or -1) != len(manifest_records):
            errors.append("summary_manifest_count_mismatch")
    return counts, errors


def _validate_promotion_record(record: dict[str, Any], blocker_ids: set[str], errors: list[str]) -> None:
    label = str(record.get("ledger_record_id") or record.get("readiness_record_id") or "")
    category = str(record.get("promotion_category") or "")
    _validate_common_flags(record, errors)
    if category not in PROMOTION_CATEGORIES:
        errors.append(f"invalid_promotion_category:{label}")
    if category != "ready_for_manifest" and record.get("usable_as_experiment_seed") is not False:
        errors.append(f"unexpected_seed_ready:{label}")
    if category == "ready_for_manifest" and record.get("usable_as_experiment_seed") is not True:
        errors.append(f"ready_record_not_seed_ready:{label}")
    if category.startswith("blocked_") or category in {"deferred", "quarantined_false_positive", "rejected"}:
        if not record.get("blockers"):
            errors.append(f"blockers_missing:{label}")
    for blocker_id in record.get("blocker_ids") or []:
        if str(blocker_id) not in blocker_ids:
            errors.append(f"unknown_blocker_id:{label}:{blocker_id}")


def _validate_common_flags(record: dict[str, Any], errors: list[str]) -> None:
    label = str(
        record.get("ledger_record_id")
        or record.get("readiness_record_id")
        or record.get("blocker_record_id")
        or record.get("manifest_readiness_id")
        or record.get("record_type")
    )
    for key in ("execution_enabled", "solve_claim"):
        if key in record and record.get(key) is not False:
            errors.append(f"{key}_not_false:{label}")
    for key in ("canonical_corpus_active", "page_boundaries_final", "cuda_used", "generated_outputs_committed"):
        if key in record and record.get(key) is not False:
            errors.append(f"{key}_not_false:{label}")
