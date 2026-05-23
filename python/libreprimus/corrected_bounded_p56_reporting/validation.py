"""Validation for Stage 5AE corrected bounded p56 reporting."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_records, read_yaml, resolve
from .models import (
    ARCHIVE_SOURCE_LOCK_DEFERRAL_PATH,
    COMMON_FALSE_FLAGS,
    CORRECTED_FORMULA_HASH,
    DOC_STALENESS_VALIDATION_PATH,
    EXPECTED_COUNTS,
    FORMULA_PARITY_REPORT_PATH,
    FULL_P56_BLOCKER_PATH,
    GENERATED_BODY_POLICY_PATH,
    HASH_MATERIAL_POLICY_PATH,
    HISTORICAL_COMPUTED_CUDA_HASH,
    HISTORICAL_EXPECTED_HASH,
    METHOD_STATUS_IMPACT_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    REFERENCE_CONTRACT_REPAIR_PATH,
    REPORT_FILES,
    RESULT_STORE_INTEGRATION_PATH,
    SCORE_SUMMARY_INTEGRATION_PATH,
    SCORED_EXPERIMENT_DEFERRAL_PATH,
    SELECTED_NEXT_OPTION_ID,
    SUMMARY_PATH,
)


def validate_stage5ae_results(
    *,
    formula_parity_report_path: Path = FORMULA_PARITY_REPORT_PATH,
    reference_contract_repair_path: Path = REFERENCE_CONTRACT_REPAIR_PATH,
    hash_material_policy_path: Path = HASH_MATERIAL_POLICY_PATH,
    result_store_integration_path: Path = RESULT_STORE_INTEGRATION_PATH,
    score_summary_integration_path: Path = SCORE_SUMMARY_INTEGRATION_PATH,
    method_status_impact_path: Path = METHOD_STATUS_IMPACT_PATH,
    generated_body_policy_path: Path = GENERATED_BODY_POLICY_PATH,
    full_p56_blocker_path: Path = FULL_P56_BLOCKER_PATH,
    scored_experiment_deferral_path: Path = SCORED_EXPERIMENT_DEFERRAL_PATH,
    archive_source_lock_deferral_path: Path = ARCHIVE_SOURCE_LOCK_DEFERRAL_PATH,
    doc_staleness_validation_path: Path = DOC_STALENESS_VALIDATION_PATH,
    next_stage_decision_path: Path = NEXT_STAGE_DECISION_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    groups = {
        "corrected_formula_parity_report_records": _load_records(errors, formula_parity_report_path),
        "reference_contract_repair_records": _load_records(errors, reference_contract_repair_path),
        "hash_material_policy_records": _load_records(errors, hash_material_policy_path),
        "result_store_integration_records": _load_records(errors, result_store_integration_path),
        "score_summary_integration_records": _load_records(errors, score_summary_integration_path),
        "method_status_impact_records": _load_records(errors, method_status_impact_path),
        "generated_body_policy_records": _load_records(errors, generated_body_policy_path),
        "full_p56_blocker_records": _load_records(errors, full_p56_blocker_path),
        "scored_experiment_deferral_records": _load_records(errors, scored_experiment_deferral_path),
        "archive_source_lock_deferral_records": _load_records(errors, archive_source_lock_deferral_path),
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
    _validate_formula(errors, groups["corrected_formula_parity_report_records"])
    _validate_reference_contract(errors, groups["reference_contract_repair_records"])
    _validate_hash_material_policy(errors, groups["hash_material_policy_records"])
    _validate_method_status(errors, groups["method_status_impact_records"])
    _validate_deferrals(errors, groups)
    _validate_decisions(errors, groups["next_stage_decision_records"])
    _validate_summary(errors, summary if isinstance(summary, dict) else {})
    _validate_reports(errors, results_dir)
    counts["stage5ae_valid"] = not errors
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
    if record.get("stage5ad_historical_failure_preserved") is not True:
        errors.append(f"{group}[{index}] historical_failure_not_preserved")
    if record.get("historical_stage5ad_reclassified_as_passed") is not False:
        errors.append(f"{group}[{index}] stage5ad_reclassified_as_passed")


def _validate_formula(errors: list[str], records: list[dict[str, Any]]) -> None:
    if len(records) != 1:
        return
    record = records[0]
    if record.get("historical_expected_hash") != HISTORICAL_EXPECTED_HASH:
        errors.append("historical_expected_hash_changed")
    if record.get("historical_computed_cuda_hash") != HISTORICAL_COMPUTED_CUDA_HASH:
        errors.append("historical_computed_cuda_hash_changed")
    if record.get("corrected_formula_expected_hash") != CORRECTED_FORMULA_HASH:
        errors.append("corrected_formula_expected_hash_wrong")
    if record.get("corrected_formula_computed_hash") != CORRECTED_FORMULA_HASH:
        errors.append("corrected_formula_computed_hash_wrong")
    if record.get("corrected_formula_parity_status") != "passed":
        errors.append("corrected_formula_parity_not_passed")
    if record.get("historical_expected_hash") == record.get("corrected_formula_expected_hash"):
        errors.append("historical_reference_hash_reused_as_formula_hash")


def _validate_reference_contract(errors: list[str], records: list[dict[str, Any]]) -> None:
    by_hash = {record.get("hash_value"): record for record in records}
    formula = by_hash.get(CORRECTED_FORMULA_HASH)
    reference = by_hash.get(HISTORICAL_EXPECTED_HASH)
    if formula is None or reference is None:
        errors.append("reference_contract_missing_formula_or_reference_hash")
        return
    if formula.get("valid_for_formula_parity") is not True or formula.get("valid_for_reference_parity") is not False:
        errors.append("formula_hash_role_invalid")
    if reference.get("valid_for_formula_parity") is not False or reference.get("valid_for_reference_parity") is not True:
        errors.append("reference_hash_role_invalid")


def _validate_hash_material_policy(errors: list[str], records: list[dict[str, Any]]) -> None:
    for record in records:
        forbidden = set(record.get("forbidden_comparison_contexts", []))
        if record.get("hash_material_kind") == "formula_output_tokens" and "formula_output_vs_candidate_major_reference" not in forbidden:
            errors.append("formula_policy_allows_reference_cross_use")
        if record.get("hash_material_policy_repair_complete") is not True:
            errors.append("hash_material_policy_not_complete")


def _validate_method_status(errors: list[str], records: list[dict[str, Any]]) -> None:
    if any(record.get("method_status_upgraded") is True for record in records):
        errors.append("method_status_upgraded")
    if any(record.get("solve_claim") is True for record in records):
        errors.append("method_status_claims_solve")


def _validate_deferrals(errors: list[str], groups: dict[str, list[dict[str, Any]]]) -> None:
    if groups["full_p56_blocker_records"][0].get("full_p56_cuda_allowed") is not False:
        errors.append("full_p56_not_blocked")
    if groups["scored_experiment_deferral_records"][0].get("scored_experiment_execution_allowed") is not False:
        errors.append("scored_experiment_not_deferred")
    if any(record.get("raw_archive_processed") is True for record in groups["archive_source_lock_deferral_records"]):
        errors.append("archive_raw_data_processed")


def _validate_decisions(errors: list[str], records: list[dict[str, Any]]) -> None:
    selected = [record for record in records if record.get("selected") is True]
    if len(selected) != 1:
        errors.append(f"selected_decision_count_mismatch: {len(selected)}")
        return
    if selected[0].get("option_id") != SELECTED_NEXT_OPTION_ID:
        errors.append("wrong_stage5ae_next_stage_selected")
    if selected[0].get("archive_source_lock_ready_next") is not True:
        errors.append("archive_source_lock_not_ready_next")
    if any(record.get("execution_enabled") is True for record in records):
        errors.append("next_stage_execution_enabled")


def _validate_summary(errors: list[str], summary: dict[str, Any]) -> None:
    if summary.get("record_type") != "stage5ae_corrected_bounded_p56_reporting_summary":
        errors.append("summary_record_type_unexpected")
    if summary.get("stage_id") != "stage-5ae" or summary.get("status") != "complete":
        errors.append("summary_stage_or_status_unexpected")
    if summary.get("historical_stage5ad_failure_preserved") is not True:
        errors.append("summary_historical_failure_not_preserved")
    if summary.get("historical_stage5ad_status") != "failed_hash_mismatch":
        errors.append("summary_stage5ad_status_not_failed")
    if summary.get("corrected_formula_parity_status") != "passed":
        errors.append("summary_corrected_formula_not_passed")
    if summary.get("corrected_formula_expected_hash") != CORRECTED_FORMULA_HASH:
        errors.append("summary_corrected_expected_hash_wrong")
    if summary.get("corrected_formula_computed_hash") != CORRECTED_FORMULA_HASH:
        errors.append("summary_corrected_computed_hash_wrong")
    for key, expected in COMMON_FALSE_FLAGS.items():
        if summary.get(key) is not expected:
            errors.append(f"summary_guardrail_violation: {key}={summary.get(key)}")
    if summary.get("new_cuda_kernels_added") != 0:
        errors.append("summary_new_cuda_kernel_added")
    if summary.get("reference_contract_repair_complete") is not True:
        errors.append("summary_reference_contract_repair_incomplete")
    if summary.get("hash_material_policy_repair_complete") is not True:
        errors.append("summary_hash_material_policy_incomplete")


def _validate_reports(errors: list[str], results_dir: Path) -> None:
    resolved = resolve(results_dir)
    for filename in REPORT_FILES.values():
        if not (resolved / filename).exists():
            errors.append(f"missing_generated_report: {resolved / filename}")
