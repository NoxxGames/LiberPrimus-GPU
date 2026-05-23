"""Stage 5AF validation helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_records, read_yaml, resolve
from .manifest import validate_manifest
from .models import (
    COMMON_FALSE_FLAGS,
    DRY_RUN_SUMMARY_REPORT,
    FAILURES_REPORT,
    HARVEST_PLAN_REPORT,
    MANIFEST_VALIDATION_REPORT,
    RESEARCH_BUNDLE_PLAN_REPORT,
    REQUIRED_BUNDLE_IDS,
    REQUIRED_SOURCE_IDS,
    SUMMARY_REPORT,
    WARNINGS_REPORT,
)


def validate_stage5af(
    *,
    source_manifest_path: Path,
    collection_priorities_path: Path,
    clue_target_categories_path: Path,
    research_bundle_plan_path: Path,
    tool_policy_path: Path,
    dry_run_summary_path: Path,
    next_stage_decision_path: Path,
    summary_path: Path,
    results_dir: Path,
) -> tuple[dict[str, Any], list[str]]:
    """Validate committed Stage 5AF records and generated local reports."""

    errors: list[str] = []
    manifest_summary, manifest_errors = validate_manifest(source_manifest_path, out_dir=results_dir)
    errors.extend(manifest_errors)
    sources = _safe_records(errors, source_manifest_path)
    priorities = _safe_records(errors, collection_priorities_path)
    categories = _safe_records(errors, clue_target_categories_path)
    bundles = _safe_records(errors, research_bundle_plan_path)
    decisions = _safe_records(errors, next_stage_decision_path)
    tool_policy = _safe_yaml(errors, tool_policy_path)
    dry_run = _safe_yaml(errors, dry_run_summary_path)
    summary = _safe_yaml(errors, summary_path)

    source_ids = {record.get("source_id") for record in sources}
    if not REQUIRED_SOURCE_IDS.issubset(source_ids):
        errors.append("required_source_ids_missing")
    bundle_ids = {record.get("bundle_id") for record in bundles}
    if not REQUIRED_BUNDLE_IDS.issubset(bundle_ids):
        errors.append("required_bundle_ids_missing")
    _validate_policy(errors, tool_policy)
    _validate_summary_guardrails(errors, summary)
    _validate_decisions(errors, decisions)
    if dry_run.get("network_fetch_performed") is not False:
        errors.append("dry_run_network_fetch_performed")
    if summary.get("source_manifest_records") != len(sources):
        errors.append("summary_source_manifest_count_mismatch")
    if summary.get("collection_priority_records") != len(priorities):
        errors.append("summary_collection_priority_count_mismatch")
    if summary.get("clue_target_category_records") != len(categories):
        errors.append("summary_clue_category_count_mismatch")
    if summary.get("research_bundle_plan_records") != len(bundles):
        errors.append("summary_bundle_count_mismatch")

    for filename in (
        HARVEST_PLAN_REPORT,
        MANIFEST_VALIDATION_REPORT,
        DRY_RUN_SUMMARY_REPORT,
        RESEARCH_BUNDLE_PLAN_REPORT,
        SUMMARY_REPORT,
        WARNINGS_REPORT,
        FAILURES_REPORT,
    ):
        if not (resolve(results_dir) / filename).exists():
            errors.append(f"missing_generated_report:{filename}")

    counts = {
        "source_manifest_records": len(sources),
        "collection_priority_records": len(priorities),
        "clue_target_category_records": len(categories),
        "research_bundle_plan_records": len(bundles),
        "dry_run_plan_records": dry_run.get("dry_run_plan_records", 0),
        "source_manifest_required_ids_present": manifest_summary.get("required_source_ids_present"),
        "network_fetch_performed": summary.get("network_fetch_performed"),
        "raw_downloads_committed": summary.get("raw_downloads_committed"),
        "raw_archives_processed": summary.get("raw_archives_processed"),
        "stage5af_valid": not errors,
    }
    return counts, errors


def _safe_records(errors: list[str], path: Path) -> list[dict[str, Any]]:
    try:
        return read_records(path)
    except (OSError, ValueError) as exc:
        errors.append(f"record_load_failed:{path}:{exc}")
        return []


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


def _validate_policy(errors: list[str], policy: dict[str, Any]) -> None:
    required_false = (
        "default_network_allowed",
        "default_download_allowed",
        "default_browser_allowed",
        "default_raw_commit_allowed",
        "default_raw_archive_processing_allowed",
        "google_drive_storage_allowed",
    )
    for key in required_false:
        if policy.get(key) is not False:
            errors.append(f"tool_policy_{key}_must_be_false")
    required_true = (
        "requires_output_root_for_fetch",
        "requires_rate_limit",
        "requires_failure_log",
        "requires_hash_inventory",
        "requires_source_tier",
        "requires_manual_export_notice_for_google",
        "requires_no_credentials",
        "requires_no_access_control_bypass",
        "requires_no_ci_network",
        "local_storage_only",
    )
    for key in required_true:
        if policy.get(key) is not True:
            errors.append(f"tool_policy_{key}_must_be_true")


def _validate_summary_guardrails(errors: list[str], summary: dict[str, Any]) -> None:
    if summary.get("record_type") != "stage5af_source_harvester_summary":
        errors.append("summary_record_type_unexpected")
    if summary.get("stage_id") != "stage-5af" or summary.get("status") != "complete":
        errors.append("summary_stage_or_status_unexpected")
    for key, expected in COMMON_FALSE_FLAGS.items():
        if summary.get(key) is not expected:
            errors.append(f"summary_guardrail_violation:{key}={summary.get(key)}")
    if summary.get("new_cuda_kernels_added") != 0:
        errors.append("summary_new_cuda_kernels_added")
    if summary.get("no_solve_claim") is not True:
        errors.append("summary_no_solve_claim_not_true")
    if summary.get("google_drive_storage_allowed") is not False:
        errors.append("summary_google_drive_storage_allowed")
    if summary.get("local_storage_only") is not True:
        errors.append("summary_local_storage_only_not_true")


def _validate_decisions(errors: list[str], decisions: list[dict[str, Any]]) -> None:
    selected = [record for record in decisions if record.get("selected") is True]
    if len(selected) != 1:
        errors.append(f"selected_decision_count_mismatch:{len(selected)}")
        return
    if selected[0].get("option_id") != "stage5ag_run_source_harvester_on_user_downloads":
        errors.append("wrong_next_stage_selected")
    if selected[0].get("deep_research_recommended_next") is not False:
        errors.append("deep_research_recommended_too_early")
    if any(record.get("execution_enabled") is True for record in decisions):
        errors.append("next_stage_execution_enabled")
