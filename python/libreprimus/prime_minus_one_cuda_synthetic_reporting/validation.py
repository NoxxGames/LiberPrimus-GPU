"""Validation for Stage 5AC reporting records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_cuda_synthetic_reporting.export import read_records, read_yaml, resolve
from libreprimus.prime_minus_one_cuda_synthetic_reporting.models import (
    BOUNDED_P56_PREFLIGHT_PATH,
    COMMON_FALSE_FLAGS,
    DOC_STALENESS_VALIDATION_PATH,
    EXPECTED_BOUNDED_P56_HASH,
    EXPECTED_COUNTS,
    EXPECTED_SYNTHETIC_HASH,
    FULL_P56_BLOCKER_PATH,
    GENERATED_BODY_POLICY_PATH,
    METHOD_STATUS_IMPACT_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    PARITY_REPORT_PATH,
    REPORT_FILES,
    RESULT_STORE_INTEGRATION_PATH,
    SCORE_SUMMARY_INTEGRATION_PATH,
    SCORED_EXPERIMENT_DEFERRAL_PATH,
    SUMMARY_PATH,
)


def validate_stage5ac_results(
    *,
    parity_report_path: Path = PARITY_REPORT_PATH,
    result_store_integration_path: Path = RESULT_STORE_INTEGRATION_PATH,
    score_summary_integration_path: Path = SCORE_SUMMARY_INTEGRATION_PATH,
    method_status_impact_path: Path = METHOD_STATUS_IMPACT_PATH,
    generated_body_policy_path: Path = GENERATED_BODY_POLICY_PATH,
    bounded_p56_preflight_path: Path = BOUNDED_P56_PREFLIGHT_PATH,
    full_p56_blocker_path: Path = FULL_P56_BLOCKER_PATH,
    scored_experiment_deferral_path: Path = SCORED_EXPERIMENT_DEFERRAL_PATH,
    doc_staleness_validation_path: Path = DOC_STALENESS_VALIDATION_PATH,
    next_stage_decision_path: Path = NEXT_STAGE_DECISION_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    groups = {
        "synthetic_parity_report_records": _load_records(errors, parity_report_path),
        "result_store_integration_records": _load_records(errors, result_store_integration_path),
        "score_summary_integration_records": _load_records(errors, score_summary_integration_path),
        "method_status_impact_records": _load_records(errors, method_status_impact_path),
        "generated_body_policy_records": _load_records(errors, generated_body_policy_path),
        "bounded_p56_preflight_records": _load_records(errors, bounded_p56_preflight_path),
        "full_p56_blocker_records": _load_records(errors, full_p56_blocker_path),
        "scored_experiment_deferral_records": _load_records(errors, scored_experiment_deferral_path),
        "doc_staleness_validation_records": _load_records(errors, doc_staleness_validation_path),
        "next_stage_decision_records": _load_records(errors, next_stage_decision_path),
    }
    try:
        summary = read_yaml(summary_path)
    except (OSError, ValueError) as exc:
        summary = {}
        errors.append(f"summary_load_failed: {exc}")
    counts = {key: len(records) for key, records in groups.items()}
    for key, expected in EXPECTED_COUNTS.items():
        if counts.get(key) != expected:
            errors.append(f"{key}_count_mismatch: {counts.get(key)} != {expected}")
        if isinstance(summary, dict) and summary.get(key) != expected:
            errors.append(f"{key}_summary_mismatch: {summary.get(key)} != {expected}")
    for group, records in groups.items():
        for index, record in enumerate(records):
            _check_guardrails(errors, group, index, record)
    _validate_parity(errors, groups["synthetic_parity_report_records"])
    _validate_bounded_p56(errors, groups["bounded_p56_preflight_records"])
    _validate_full_p56(errors, groups["full_p56_blocker_records"])
    _validate_deferrals(errors, groups["scored_experiment_deferral_records"])
    _validate_doc_staleness(errors, groups["doc_staleness_validation_records"])
    _validate_decisions(errors, groups["next_stage_decision_records"])
    _validate_summary(errors, summary if isinstance(summary, dict) else {})
    _validate_reports(errors, results_dir)
    counts["stage5ac_valid"] = not errors
    return counts, errors


def _load_records(errors: list[str], path: Path) -> list[dict[str, Any]]:
    try:
        return read_records(path)
    except (OSError, ValueError) as exc:
        errors.append(f"record_load_failed: {path}: {exc}")
        return []


def _check_guardrails(errors: list[str], group: str, index: int, record: dict[str, Any]) -> None:
    for key, expected in COMMON_FALSE_FLAGS.items():
        if record.get(key) is not expected:
            errors.append(f"{group}[{index}] guardrail_violation: {key}={record.get(key)}")
    if record.get("no_solve_claim") is not True:
        errors.append(f"{group}[{index}] no_solve_claim_not_true")
    if record.get("metadata_only") is not True or record.get("reporting_only") is not True:
        errors.append(f"{group}[{index}] not_reporting_metadata_only")


def _validate_parity(errors: list[str], records: list[dict[str, Any]]) -> None:
    if len(records) != 1:
        return
    record = records[0]
    if record.get("parity_status") != "passed":
        errors.append("synthetic_parity_not_passed")
    if record.get("expected_output_token_hash") != EXPECTED_SYNTHETIC_HASH:
        errors.append("synthetic_expected_hash_mismatch")
    if record.get("computed_output_token_hash") != EXPECTED_SYNTHETIC_HASH:
        errors.append("synthetic_computed_hash_mismatch")
    if record.get("stage5aa_hash_match") is not True:
        errors.append("stage5aa_hash_match_not_true")


def _validate_bounded_p56(errors: list[str], records: list[dict[str, Any]]) -> None:
    if len(records) != 1:
        return
    record = records[0]
    if record.get("expected_output_token_hash") != EXPECTED_BOUNDED_P56_HASH:
        errors.append("bounded_p56_expected_hash_mismatch")
    if record.get("bounded_p56_cuda_execution_allowed_current_stage") is not False:
        errors.append("bounded_p56_execution_allowed_current_stage")
    if record.get("preflight_status") != "ready_for_stage5ad_bounded_p56_cuda_parity":
        errors.append("bounded_p56_preflight_not_ready")
    if record.get("bounded_p56_cuda_execution_ready_next_stage") is not True:
        errors.append("bounded_p56_ready_next_stage_not_true")


def _validate_full_p56(errors: list[str], records: list[dict[str, Any]]) -> None:
    if len(records) == 1 and records[0].get("full_p56_status") != "blocked_full_p56_token_buffer_missing":
        errors.append("full_p56_not_blocked")


def _validate_deferrals(errors: list[str], records: list[dict[str, Any]]) -> None:
    if any(record.get("execution_enabled") is not False for record in records):
        errors.append("scored_deferral_allows_execution")
    if not any(record.get("experiment_class") == "website_expansion" and record.get("deferral_status") == "deferred_future_unnumbered_project" for record in records):
        errors.append("website_expansion_deferral_missing")


def _validate_doc_staleness(errors: list[str], records: list[dict[str, Any]]) -> None:
    if len(records) == 1 and records[0].get("doc_staleness_strict_check_passed") is not True:
        errors.append("doc_staleness_not_clean")


def _validate_decisions(errors: list[str], records: list[dict[str, Any]]) -> None:
    selected = [record for record in records if record.get("selected") is True]
    if len(selected) != 1:
        errors.append(f"selected_decision_count_mismatch: {len(selected)}")
        return
    if selected[0].get("option_id") != "stage5ad_bounded_p56_cuda_parity_run":
        errors.append("bounded_p56_cuda_parity_not_selected")
    if selected[0].get("future_cuda_execution_allowed") is not True:
        errors.append("selected_future_cuda_not_allowed_for_next_stage")
    if any(record.get("benchmark_execution_allowed") is True or record.get("scored_experiment_execution_allowed") is True for record in records):
        errors.append("forbidden_decision_execution_allowed")


def _validate_summary(errors: list[str], summary: dict[str, Any]) -> None:
    if summary.get("record_type") != "stage5ac_prime_minus_one_cuda_synthetic_reporting_summary":
        errors.append("summary_record_type_unexpected")
    if summary.get("stage_id") != "stage-5ac" or summary.get("status") != "complete":
        errors.append("summary_stage_or_status_unexpected")
    for key, expected in COMMON_FALSE_FLAGS.items():
        if summary.get(key) is not expected:
            errors.append(f"summary_guardrail_violation: {key}={summary.get(key)}")
    if summary.get("stage5aa_hash_match") is not True:
        errors.append("summary_stage5aa_hash_match_not_true")
    if summary.get("stage5ab_doc_staleness_strict_pass") is not True:
        errors.append("summary_doc_staleness_not_true")
    if summary.get("recommended_next_stage_title") != "Stage 5AD - bounded p56 CUDA parity run":
        errors.append("summary_next_stage_unexpected")


def _validate_reports(errors: list[str], results_dir: Path) -> None:
    resolved = resolve(results_dir)
    for filename in REPORT_FILES.values():
        if not (resolved / filename).exists():
            errors.append(f"missing_generated_report: {resolved / filename}")
