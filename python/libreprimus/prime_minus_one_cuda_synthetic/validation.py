"""Validation for Stage 5AA prime-minus-one CUDA synthetic records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_cuda_synthetic.export import read_records, read_yaml, resolve
from libreprimus.prime_minus_one_cuda_synthetic.models import (
    DEVICE_SUBSET_AUDIT_PATH,
    EXPECTED_COUNTS,
    EXPECTED_SYNTHETIC_HASH,
    FORBIDDEN_FALSE_FLAGS,
    KERNEL_IMPLEMENTATION_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    P56_BLOCKER_PATH,
    PARITY_PATH,
    REPORT_FILES,
    RESULT_STORE_PREFLIGHT_PATH,
    SCORED_EXPERIMENT_DEFERRAL_PATH,
    SUMMARY_PATH,
    CUDA_RUN_PATH,
)


def validate_stage5aa_results(
    *,
    kernel_implementation_path: Path = KERNEL_IMPLEMENTATION_PATH,
    cuda_run_path: Path = CUDA_RUN_PATH,
    parity_path: Path = PARITY_PATH,
    device_subset_audit_path: Path = DEVICE_SUBSET_AUDIT_PATH,
    result_store_preflight_path: Path = RESULT_STORE_PREFLIGHT_PATH,
    p56_blocker_path: Path = P56_BLOCKER_PATH,
    scored_experiment_deferral_path: Path = SCORED_EXPERIMENT_DEFERRAL_PATH,
    next_stage_decision_path: Path = NEXT_STAGE_DECISION_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    groups = {
        "kernel_implementation_records": _load_records(errors, kernel_implementation_path),
        "cuda_run_records": _load_records(errors, cuda_run_path),
        "parity_records": _load_records(errors, parity_path),
        "device_subset_audit_records": _load_records(errors, device_subset_audit_path),
        "result_store_preflight_records": _load_records(errors, result_store_preflight_path),
        "p56_blocker_records": _load_records(errors, p56_blocker_path),
        "scored_experiment_deferral_records": _load_records(errors, scored_experiment_deferral_path),
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
    _validate_kernel(errors, groups["kernel_implementation_records"])
    _validate_run_and_parity(errors, groups["cuda_run_records"], groups["parity_records"])
    _validate_device_audit(errors, groups["device_subset_audit_records"])
    _validate_blockers(errors, groups["p56_blocker_records"], groups["scored_experiment_deferral_records"])
    _validate_next_stage(errors, groups["next_stage_decision_records"], groups["parity_records"], summary if isinstance(summary, dict) else {})
    _validate_summary(errors, summary if isinstance(summary, dict) else {})
    _validate_reports(errors, results_dir)
    counts["stage5aa_valid"] = not errors
    return counts, errors


def _load_records(errors: list[str], path: Path) -> list[dict[str, Any]]:
    try:
        return read_records(path)
    except (OSError, ValueError) as exc:
        errors.append(f"record_load_failed: {path}: {exc}")
        return []


def _check_guardrails(errors: list[str], group: str, index: int, record: dict[str, Any]) -> None:
    for key in FORBIDDEN_FALSE_FLAGS:
        if record.get(key) is not False:
            errors.append(f"{group}[{index}] guardrail_violation: {key}={record.get(key)}")
    if record.get("no_solve_claim") is not True:
        errors.append(f"{group}[{index}] no_solve_claim_not_true")
    if record.get("new_cuda_kernels_added") != 1:
        errors.append(f"{group}[{index}] new_cuda_kernel_count_not_one")
    if record.get("synthetic_only") is not True:
        errors.append(f"{group}[{index}] synthetic_only_not_true")


def _validate_kernel(errors: list[str], records: list[dict[str, Any]]) -> None:
    if len(records) != 1:
        return
    record = records[0]
    if record.get("implementation_status") != "implemented_synthetic_only":
        errors.append("kernel_implementation_status_unexpected")
    if record.get("p56_cuda_allowed") is not False or record.get("full_p56_cuda_allowed") is not False:
        errors.append("kernel_allows_p56_scope")


def _validate_run_and_parity(
    errors: list[str],
    runs: list[dict[str, Any]],
    parity_records: list[dict[str, Any]],
) -> None:
    if len(runs) != 1 or len(parity_records) != 1:
        return
    run = runs[0]
    parity = parity_records[0]
    if run.get("validation_vector_id") != "stage5z-validation-synthetic-prime-control-v0":
        errors.append("unexpected_validation_vector_executed")
    computed = parity.get("computed_output_token_hash")
    status = parity.get("parity_status")
    if status == "passed" and computed != EXPECTED_SYNTHETIC_HASH:
        errors.append("passed_parity_without_expected_hash")
    if computed and computed != EXPECTED_SYNTHETIC_HASH and status != "failed_hash_mismatch":
        errors.append("hash_mismatch_not_marked_failed")
    if int(run.get("cuda_pass_count", 0)) and status != "passed":
        errors.append("cuda_pass_count_without_passed_parity")


def _validate_device_audit(errors: list[str], records: list[dict[str, Any]]) -> None:
    if len(records) == 1 and records[0].get("forbidden_finding_count") != 0:
        errors.append("device_subset_audit_findings_present")


def _validate_blockers(
    errors: list[str],
    p56_blockers: list[dict[str, Any]],
    scored_deferrals: list[dict[str, Any]],
) -> None:
    if not any(record.get("blocker_status") == "blocked_full_p56_token_buffer_missing" for record in p56_blockers):
        errors.append("full_p56_blocker_missing")
    if any(record.get("execution_enabled") is not False for record in scored_deferrals):
        errors.append("scored_deferral_allows_execution")


def _validate_next_stage(
    errors: list[str],
    decisions: list[dict[str, Any]],
    parity_records: list[dict[str, Any]],
    summary: dict[str, Any],
) -> None:
    selected = [record for record in decisions if record.get("selected") is True]
    if len(selected) != 1:
        errors.append(f"selected_next_stage_count_mismatch: {len(selected)}")
        return
    parity_status = parity_records[0].get("parity_status") if parity_records else None
    option_id = selected[0].get("option_id")
    if parity_status == "passed" and option_id != "stage5ab_prime_minus_one_synthetic_reporting_bounded_p56_preflight":
        errors.append("passed_parity_did_not_select_stage5ab")
    if parity_status != "passed" and option_id == "stage5ab_prime_minus_one_synthetic_reporting_bounded_p56_preflight":
        errors.append("stage5ab_selected_without_passed_parity")
    if summary.get("recommended_next_stage_title") != selected[0].get("recommended_stage_title"):
        errors.append("summary_next_stage_mismatch")
    if any(record.get("benchmark_selected") is True or record.get("scored_experiment_selected") is True for record in decisions):
        errors.append("forbidden_next_stage_selected")


def _validate_summary(errors: list[str], summary: dict[str, Any]) -> None:
    if summary.get("stage_id") != "stage-5aa" or summary.get("status") != "complete":
        errors.append("summary_stage_or_status_unexpected")
    for key in FORBIDDEN_FALSE_FLAGS:
        if summary.get(key) is not False:
            errors.append(f"summary_guardrail_violation: {key}={summary.get(key)}")
    if summary.get("new_cuda_kernels_added") != 1:
        errors.append("summary_new_cuda_kernel_count_unexpected")


def _validate_reports(errors: list[str], results_dir: Path) -> None:
    resolved = resolve(results_dir)
    for filename in REPORT_FILES.values():
        if not (resolved / filename).exists():
            errors.append(f"missing_generated_report: {resolved / filename}")
