"""Validation for Stage 5AD bounded p56 CUDA parity records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_records, read_yaml, resolve
from .models import (
    COMMON_FALSE_FLAGS,
    CUDA_PARITY_PATH,
    CUDA_RUN_PATH,
    DEVICE_SUBSET_AUDIT_PATH,
    DOC_STALENESS_VALIDATION_PATH,
    EXPECTED_COUNTS,
    EXPECTED_OUTPUT_TOKEN_HASH,
    FULL_P56_BLOCKER_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    REPORT_FILES,
    RESULT_STORE_PREFLIGHT_PATH,
    SCORE_SUMMARY_PREFLIGHT_PATH,
    SCORED_EXPERIMENT_DEFERRAL_PATH,
    SUMMARY_PATH,
    VALIDATION_VECTOR_ID,
)


def validate_stage5ad_results(
    *,
    cuda_run_path: Path = CUDA_RUN_PATH,
    cuda_parity_path: Path = CUDA_PARITY_PATH,
    result_store_preflight_path: Path = RESULT_STORE_PREFLIGHT_PATH,
    score_summary_preflight_path: Path = SCORE_SUMMARY_PREFLIGHT_PATH,
    full_p56_blocker_path: Path = FULL_P56_BLOCKER_PATH,
    scored_experiment_deferral_path: Path = SCORED_EXPERIMENT_DEFERRAL_PATH,
    doc_staleness_validation_path: Path = DOC_STALENESS_VALIDATION_PATH,
    device_subset_audit_path: Path = DEVICE_SUBSET_AUDIT_PATH,
    next_stage_decision_path: Path = NEXT_STAGE_DECISION_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    groups = {
        "cuda_run_records": _load_records(errors, cuda_run_path),
        "cuda_parity_records": _load_records(errors, cuda_parity_path),
        "result_store_preflight_records": _load_records(errors, result_store_preflight_path),
        "score_summary_preflight_records": _load_records(errors, score_summary_preflight_path),
        "full_p56_blocker_records": _load_records(errors, full_p56_blocker_path),
        "scored_experiment_deferral_records": _load_records(errors, scored_experiment_deferral_path),
        "doc_staleness_validation_records": _load_records(errors, doc_staleness_validation_path),
        "device_subset_audit_records": _load_records(errors, device_subset_audit_path),
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
    _validate_run(errors, groups["cuda_run_records"])
    _validate_parity(errors, groups["cuda_parity_records"], groups["cuda_run_records"])
    _validate_full_p56(errors, groups["full_p56_blocker_records"])
    _validate_deferrals(errors, groups["scored_experiment_deferral_records"])
    _validate_doc_staleness(errors, groups["doc_staleness_validation_records"])
    _validate_audit(errors, groups["device_subset_audit_records"])
    _validate_decisions(errors, groups["next_stage_decision_records"], groups["cuda_parity_records"])
    _validate_summary(errors, summary if isinstance(summary, dict) else {})
    _validate_reports(errors, results_dir)
    counts["stage5ad_valid"] = not errors
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
    if record.get("new_cuda_kernel_added") is not False or record.get("new_cuda_kernels_added") != 0:
        errors.append(f"{group}[{index}] new_cuda_kernel_added")
    if record.get("device_kernel_arithmetic_modified") is not False:
        errors.append(f"{group}[{index}] device_arithmetic_modified")


def _validate_run(errors: list[str], records: list[dict[str, Any]]) -> None:
    if len(records) != 1:
        return
    record = records[0]
    if record.get("validation_vector_id") != VALIDATION_VECTOR_ID:
        errors.append("wrong_validation_vector_executed")
    if record.get("expected_output_token_hash") != EXPECTED_OUTPUT_TOKEN_HASH:
        errors.append("run_expected_hash_mismatch")
    if record.get("cuda_execution_status") == "passed" and record.get("computed_cuda_output_token_hash") != EXPECTED_OUTPUT_TOKEN_HASH:
        errors.append("run_claims_pass_without_expected_hash")
    if record.get("cuda_skip_count", 0) > 0 and record.get("cuda_execution_status") == "passed":
        errors.append("skipped_run_claims_pass")


def _validate_parity(errors: list[str], records: list[dict[str, Any]], run_records: list[dict[str, Any]]) -> None:
    if len(records) != 1 or len(run_records) != 1:
        return
    parity = records[0]
    run = run_records[0]
    if parity.get("expected_output_token_hash") != EXPECTED_OUTPUT_TOKEN_HASH:
        errors.append("parity_expected_hash_mismatch")
    if parity.get("computed_cuda_output_token_hash") != run.get("computed_cuda_output_token_hash"):
        errors.append("parity_run_hash_mismatch")
    if parity.get("parity_status") == "passed" and parity.get("stage5x_expected_hash_match") is not True:
        errors.append("parity_claims_pass_without_stage5x_match")
    if parity.get("stage5aa_synthetic_rerun_in_stage5ad") is not False:
        errors.append("synthetic_rerun_counted_in_stage5ad")


def _validate_full_p56(errors: list[str], records: list[dict[str, Any]]) -> None:
    if len(records) == 1 and records[0].get("full_p56_status") != "blocked_full_p56_token_buffer_missing":
        errors.append("full_p56_not_blocked")


def _validate_deferrals(errors: list[str], records: list[dict[str, Any]]) -> None:
    if any(record.get("execution_enabled") is not False for record in records):
        errors.append("deferral_allows_execution")
    required = {"website_expansion", "visual_clue_deep_research", "cuda_scored_experiment", "benchmark_experiment"}
    present = {str(record.get("experiment_class")) for record in records}
    missing = required - present
    if missing:
        errors.append(f"missing_deferrals: {sorted(missing)}")


def _validate_doc_staleness(errors: list[str], records: list[dict[str, Any]]) -> None:
    if len(records) == 1 and records[0].get("doc_staleness_strict_check_passed") is not True:
        errors.append("doc_staleness_not_clean")


def _validate_audit(errors: list[str], records: list[dict[str, Any]]) -> None:
    if len(records) != 1:
        return
    record = records[0]
    if record.get("cuda_source_modified") is not False:
        errors.append("cuda_source_modified_unexpected")
    if record.get("new_cuda_kernels_added") != 0:
        errors.append("new_cuda_kernel_added_unexpected")


def _validate_decisions(errors: list[str], records: list[dict[str, Any]], parity_records: list[dict[str, Any]]) -> None:
    selected = [record for record in records if record.get("selected") is True]
    if len(selected) != 1:
        errors.append(f"selected_decision_count_mismatch: {len(selected)}")
        return
    parity_status = parity_records[0].get("parity_status") if parity_records else None
    selected_id = selected[0].get("option_id")
    if parity_status == "passed" and selected_id != "stage5ae_bounded_p56_cuda_parity_reporting_integration":
        errors.append("passed_parity_did_not_select_stage5ae")
    if parity_status == "failed_hash_mismatch" and selected_id != "stage5ad_fix_bounded_p56_cuda_mismatch_investigation":
        errors.append("mismatch_did_not_select_fix")
    if parity_status not in {"passed", "failed_hash_mismatch"} and selected_id != "stage5ad_followup_bounded_p56_cuda_toolchain_repair":
        errors.append("skip_did_not_select_followup")
    if any(record.get("benchmark_execution_allowed") is True or record.get("scored_experiment_execution_allowed") is True for record in records):
        errors.append("forbidden_decision_execution_allowed")


def _validate_summary(errors: list[str], summary: dict[str, Any]) -> None:
    if summary.get("record_type") != "stage5ad_bounded_p56_cuda_parity_summary":
        errors.append("summary_record_type_unexpected")
    if summary.get("stage_id") != "stage-5ad" or summary.get("status") != "complete":
        errors.append("summary_stage_or_status_unexpected")
    if summary.get("expected_output_token_hash") != EXPECTED_OUTPUT_TOKEN_HASH:
        errors.append("summary_expected_hash_mismatch")
    for key, expected in COMMON_FALSE_FLAGS.items():
        if summary.get(key) is not expected:
            errors.append(f"summary_guardrail_violation: {key}={summary.get(key)}")
    if summary.get("new_cuda_kernels_added") != 0:
        errors.append("summary_new_cuda_kernel_added")
    if summary.get("stage5ad_parity_status") == "passed" and summary.get("stage5ae_ready") is not True:
        errors.append("passed_summary_not_stage5ae_ready")


def _validate_reports(errors: list[str], results_dir: Path) -> None:
    resolved = resolve(results_dir)
    for filename in REPORT_FILES.values():
        if not (resolved / filename).exists():
            errors.append(f"missing_generated_report: {resolved / filename}")
