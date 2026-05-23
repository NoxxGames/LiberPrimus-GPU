"""Validation helpers for Stage 5AG local source inventory."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_records, read_yaml, resolve
from .models import (
    FULL_ARCHIVE_INVENTORY_REPORT,
    FULL_FILE_INVENTORY_REPORT,
    FULL_HASH_INVENTORY_REPORT,
    RESEARCH_BUNDLE_READINESS_REPORT,
    SOURCE_MANIFEST_LINKAGE_REPORT,
    STAGE5AG_FALSE_FLAGS,
    SUMMARY_REPORT,
)


def validate_stage5ag(
    *,
    root_inventory_path: Path,
    file_summary_path: Path,
    archive_summary_path: Path,
    hash_summary_path: Path,
    local_linkage_path: Path,
    candidate_summary_path: Path,
    gap_report_path: Path,
    bundle_readiness_path: Path,
    guardrail_path: Path,
    next_stage_decision_path: Path,
    summary_path: Path,
    results_dir: Path,
) -> tuple[dict[str, Any], list[str]]:
    """Validate committed Stage 5AG records and ignored generated reports."""

    errors: list[str] = []
    root = _safe_yaml(errors, root_inventory_path)
    file_summary = _safe_yaml(errors, file_summary_path)
    archive_summary = _safe_yaml(errors, archive_summary_path)
    hash_summary = _safe_yaml(errors, hash_summary_path)
    linkage = _safe_yaml(errors, local_linkage_path)
    candidates = _safe_yaml(errors, candidate_summary_path)
    gaps = _safe_yaml(errors, gap_report_path)
    bundles = _safe_yaml(errors, bundle_readiness_path)
    guardrail = _safe_yaml(errors, guardrail_path)
    decisions = _safe_records(errors, next_stage_decision_path)
    summary = _safe_yaml(errors, summary_path)

    for key, expected in STAGE5AG_FALSE_FLAGS.items():
        if key == "third_party_raw_tracked_new":
            continue
        if guardrail.get(key) is not expected:
            errors.append(f"guardrail_violation:{key}={guardrail.get(key)}")
    if guardrail.get("google_drive_storage_used") is not False:
        errors.append("google_drive_storage_used")
    if guardrail.get("source_root_raw_content_ignored") is not True:
        errors.append("source_root_raw_content_not_ignored")
    if summary.get("stage_id") != "stage-5ag" or summary.get("status") != "complete":
        errors.append("summary_stage_or_status_unexpected")
    if summary.get("total_local_files") != root.get("total_files"):
        errors.append("summary_total_local_files_mismatch")
    if summary.get("file_inventory_records") != file_summary.get("inventory_record_count"):
        errors.append("summary_file_inventory_count_mismatch")
    if summary.get("archive_file_count") != archive_summary.get("archive_record_count"):
        errors.append("summary_archive_count_mismatch")
    if summary.get("hashed_file_count") != hash_summary.get("total_hashed_files"):
        errors.append("summary_hash_count_mismatch")
    if summary.get("manifest_records_matched") != linkage.get("matched_count"):
        errors.append("summary_linkage_matched_count_mismatch")
    if summary.get("source_lock_candidates_ready") != candidates.get("ready_count"):
        errors.append("summary_candidate_ready_count_mismatch")
    if summary.get("gap_report_records") != gaps.get("gap_count"):
        errors.append("summary_gap_count_mismatch")
    if summary.get("research_bundle_records") != bundles.get("bundle_records"):
        errors.append("summary_bundle_count_mismatch")
    selected = [record for record in decisions if record.get("selected") is True]
    if len(selected) != 1:
        errors.append(f"selected_decision_count_mismatch:{len(selected)}")
    elif selected[0].get("deep_research_recommended_next") is not False:
        errors.append("deep_research_recommended_too_early")
    for filename in (
        FULL_FILE_INVENTORY_REPORT,
        FULL_HASH_INVENTORY_REPORT,
        FULL_ARCHIVE_INVENTORY_REPORT,
        SOURCE_MANIFEST_LINKAGE_REPORT,
        RESEARCH_BUNDLE_READINESS_REPORT,
        SUMMARY_REPORT,
    ):
        if not (resolve(results_dir) / filename).exists():
            errors.append(f"missing_generated_report:{filename}")

    counts = {
        "source_root_exists": root.get("root_exists"),
        "total_local_files": root.get("total_files", 0),
        "total_local_size_bytes": root.get("total_size_bytes", 0),
        "archives_inventoried": archive_summary.get("archive_record_count", 0),
        "supported_archive_count": archive_summary.get("supported_archive_count", 0),
        "unsupported_archive_count": archive_summary.get("unsupported_archive_count", 0),
        "manifest_records_matched": linkage.get("matched_count", 0),
        "manifest_records_missing": linkage.get("missing_count", 0),
        "manifest_records_ambiguous": linkage.get("ambiguous_count", 0),
        "source_lock_candidates_ready": candidates.get("ready_count", 0),
        "research_bundles_ready_for_extraction_prep": bundles.get("ready_for_extraction_prep_count", 0),
        "research_bundles_not_ready": bundles.get("not_ready_count", 0),
        "network_fetch_performed": guardrail.get("network_fetch_performed"),
        "online_repo_clone_performed": guardrail.get("online_repo_clone_performed"),
        "google_drive_storage_used": guardrail.get("google_drive_storage_used"),
        "stage5ag_valid": not errors,
    }
    return counts, errors


def _safe_yaml(errors: list[str], path: Path) -> dict[str, Any]:
    try:
        payload = read_yaml(path)
    except (OSError, ValueError) as exc:
        errors.append(f"yaml_load_failed:{path}:{exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"yaml_not_mapping:{path}")
        return {}
    return payload


def _safe_records(errors: list[str], path: Path) -> list[dict[str, Any]]:
    try:
        return read_records(path)
    except (OSError, ValueError) as exc:
        errors.append(f"record_load_failed:{path}:{exc}")
        return []
