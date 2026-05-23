"""Validation for Stage 5AD-fix mismatch records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_records, read_yaml, resolve
from .models import (
    COMMON_FALSE_FLAGS,
    EXPECTED_COUNTS,
    FORMULA_TRACE_PATH,
    GUARDRAIL_PATH,
    HASH_LINEAGE_PATH,
    HASH_MATERIAL_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    RECOMMENDED_NEXT_OPTION_ID,
    REFERENCE_CONTRACT_PATH,
    REPAIR_READINESS_PATH,
    REPORT_FILES,
    ROOT_CAUSE_PATH,
    STAGE5AD_COMPUTED_CUDA_HASH,
    STAGE5AD_EXPECTED_HASH,
    STAGE5X_FORMULA_HASH,
    STREAM_TRACE_PATH,
    SUMMARY_PATH,
    TOKEN_TRACE_PATH,
)


def validate_stage5ad_fix_results(
    *,
    hash_lineage_path: Path = HASH_LINEAGE_PATH,
    token_trace_path: Path = TOKEN_TRACE_PATH,
    stream_trace_path: Path = STREAM_TRACE_PATH,
    formula_trace_path: Path = FORMULA_TRACE_PATH,
    hash_material_path: Path = HASH_MATERIAL_PATH,
    reference_contract_path: Path = REFERENCE_CONTRACT_PATH,
    root_cause_path: Path = ROOT_CAUSE_PATH,
    repair_readiness_path: Path = REPAIR_READINESS_PATH,
    guardrail_path: Path = GUARDRAIL_PATH,
    next_stage_decision_path: Path = NEXT_STAGE_DECISION_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    groups = {
        "hash_lineage_records": _load_records(errors, hash_lineage_path),
        "token_trace_records": _load_records(errors, token_trace_path),
        "stream_trace_records": _load_records(errors, stream_trace_path),
        "formula_trace_records": _load_records(errors, formula_trace_path),
        "hash_material_records": _load_records(errors, hash_material_path),
        "reference_contract_records": _load_records(errors, reference_contract_path),
        "root_cause_records": _load_records(errors, root_cause_path),
        "repair_readiness_records": _load_records(errors, repair_readiness_path),
        "guardrail_records": _load_records(errors, guardrail_path),
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
    _validate_formula(errors, groups["formula_trace_records"])
    _validate_reference(errors, groups["reference_contract_records"])
    _validate_root_cause(errors, groups["root_cause_records"])
    _validate_decisions(errors, groups["next_stage_decision_records"])
    _validate_summary(errors, summary if isinstance(summary, dict) else {})
    _validate_reports(errors, results_dir)
    counts["stage5ad_fix_valid"] = not errors
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


def _validate_formula(errors: list[str], records: list[dict[str, Any]]) -> None:
    if len(records) != 1:
        return
    record = records[0]
    if record.get("formula_output_token_hash") != STAGE5X_FORMULA_HASH:
        errors.append("formula_hash_not_stage5x_formula")
    if record.get("formula_output_token_hash") != STAGE5AD_COMPUTED_CUDA_HASH:
        errors.append("formula_hash_not_stage5ad_cuda_hash")
    if record.get("formula_output_token_hash") == STAGE5AD_EXPECTED_HASH:
        errors.append("formula_hash_unexpectedly_matches_stage5ad_expected")


def _validate_reference(errors: list[str], records: list[dict[str, Any]]) -> None:
    if len(records) != 1:
        return
    record = records[0]
    if record.get("cuda_formula_matches_stage5x_formula") is not True:
        errors.append("cuda_formula_does_not_match_stage5x_formula")
    if record.get("cuda_formula_matches_stage5w_expected") is not False:
        errors.append("cuda_formula_unexpectedly_matches_stage5w_expected")
    if record.get("cuda_kernel_repair_required") is not False:
        errors.append("cuda_kernel_repair_incorrectly_required")
    if record.get("reference_contract_repair_required") is not True:
        errors.append("reference_contract_repair_not_required")


def _validate_root_cause(errors: list[str], records: list[dict[str, Any]]) -> None:
    selected = [record for record in records if record.get("primary_root_cause") is True]
    if len(selected) != 1:
        errors.append(f"primary_root_cause_count_mismatch: {len(selected)}")
        return
    if selected[0].get("cause_id") != "expected_hash_reference_lineage_mismatch":
        errors.append("wrong_primary_root_cause")


def _validate_decisions(errors: list[str], records: list[dict[str, Any]]) -> None:
    selected = [record for record in records if record.get("selected") is True]
    if len(selected) != 1:
        errors.append(f"selected_decision_count_mismatch: {len(selected)}")
        return
    if selected[0].get("option_id") != RECOMMENDED_NEXT_OPTION_ID:
        errors.append("wrong_stage5ad_fix_next_stage_selected")
    if any(record.get("benchmark_execution_allowed") is True for record in records):
        errors.append("benchmark_allowed_by_decision")
    if any(record.get("scored_experiment_execution_allowed") is True for record in records):
        errors.append("scored_experiment_allowed_by_decision")


def _validate_summary(errors: list[str], summary: dict[str, Any]) -> None:
    if summary.get("record_type") != "stage5ad_fix_bounded_p56_mismatch_summary":
        errors.append("summary_record_type_unexpected")
    if summary.get("stage_id") != "stage-5ad-fix" or summary.get("status") != "complete":
        errors.append("summary_stage_or_status_unexpected")
    if summary.get("stage5ad_historical_failure_preserved") is not True:
        errors.append("stage5ad_historical_failure_not_preserved")
    if summary.get("cuda_formula_matches_stage5x_formula") is not True:
        errors.append("summary_formula_stage5x_match_missing")
    if summary.get("cuda_formula_matches_stage5w_expected") is not False:
        errors.append("summary_formula_expected_mismatch_missing")
    if summary.get("cuda_execution_performed") is not False:
        errors.append("summary_cuda_execution_performed")
    for key, expected in COMMON_FALSE_FLAGS.items():
        if key == "cuda_execution_performed":
            continue
        if summary.get(key) is not expected:
            errors.append(f"summary_guardrail_violation: {key}={summary.get(key)}")
    if summary.get("new_cuda_kernels_added") != 0:
        errors.append("summary_new_cuda_kernel_added")


def _validate_reports(errors: list[str], results_dir: Path) -> None:
    resolved = resolve(results_dir)
    for filename in REPORT_FILES.values():
        if not (resolved / filename).exists():
            errors.append(f"missing_generated_report: {resolved / filename}")
