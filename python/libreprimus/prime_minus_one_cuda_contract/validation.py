"""Validation for Stage 5Z prime-minus-one CUDA contract records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_cuda_contract.export import read_records, read_yaml, resolve
from libreprimus.prime_minus_one_cuda_contract.models import BAD_TRUE_FLAGS, EXPECTED_COUNTS, REPORT_FILES


def validate_stage5z_results(
    *,
    cuda_contract_path: Path,
    kernel_abi_path: Path,
    host_runner_contract_path: Path,
    buffer_contract_path: Path,
    validation_vectors_path: Path,
    future_parity_plan_path: Path,
    result_store_compatibility_path: Path,
    full_p56_blocker_path: Path,
    scored_experiment_deferral_path: Path,
    implementation_readiness_gate_path: Path,
    next_stage_decision_path: Path,
    summary_path: Path,
    results_dir: Path,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    groups = {
        "cuda_contract_records": _load_records(errors, cuda_contract_path),
        "kernel_abi_records": _load_records(errors, kernel_abi_path),
        "host_runner_contract_records": _load_records(errors, host_runner_contract_path),
        "buffer_contract_records": _load_records(errors, buffer_contract_path),
        "validation_vector_records": _load_records(errors, validation_vectors_path),
        "future_parity_plan_records": _load_records(errors, future_parity_plan_path),
        "result_store_compatibility_records": _load_records(errors, result_store_compatibility_path),
        "full_p56_blocker_records": _load_records(errors, full_p56_blocker_path),
        "scored_experiment_deferral_records": _load_records(errors, scored_experiment_deferral_path),
        "implementation_readiness_gate_records": _load_records(errors, implementation_readiness_gate_path),
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
    _validate_contract(errors, groups["cuda_contract_records"])
    _validate_kernel_abi(errors, groups["kernel_abi_records"])
    _validate_host_runner(errors, groups["host_runner_contract_records"])
    _validate_buffer_contract(errors, groups["buffer_contract_records"])
    _validate_validation_vectors(errors, groups["validation_vector_records"])
    _validate_future_parity(errors, groups["future_parity_plan_records"])
    _validate_result_store(errors, groups["result_store_compatibility_records"])
    _validate_full_p56(errors, groups["full_p56_blocker_records"])
    _validate_scored(errors, groups["scored_experiment_deferral_records"])
    _validate_gate(errors, groups["implementation_readiness_gate_records"])
    _validate_decisions(errors, groups["next_stage_decision_records"], summary if isinstance(summary, dict) else {})
    _validate_summary(errors, summary if isinstance(summary, dict) else {})
    _validate_reports(errors, results_dir)
    counts["stage5z_valid"] = not errors
    return counts, errors


def _load_records(errors: list[str], path: Path) -> list[dict[str, Any]]:
    try:
        return read_records(path)
    except (OSError, ValueError) as exc:
        errors.append(f"record_load_failed: {path}: {exc}")
        return []


def _check_guardrails(errors: list[str], group: str, index: int, record: dict[str, Any]) -> None:
    for key in BAD_TRUE_FLAGS:
        value = record.get(key)
        if value is True or (key == "new_cuda_kernels_added" and value not in {0, False, None}):
            errors.append(f"{group}[{index}] guardrail_violation: {key}={value}")
    if record.get("no_solve_claim") is not True:
        errors.append(f"{group}[{index}] no_solve_claim_not_true")
    if record.get("no_gpu_ci_safe") is not True:
        errors.append(f"{group}[{index}] no_gpu_ci_safe_not_true")


def _validate_contract(errors: list[str], records: list[dict[str, Any]]) -> None:
    statuses = {str(record.get("contract_status")) for record in records}
    if "complete_contract_preparation_only" not in statuses:
        errors.append("contract_preparation_record_missing")
    if "blocked_full_p56_token_buffer_missing" not in statuses:
        errors.append("full_p56_contract_blocker_missing")
    if any(record.get("implementation_allowed") is not False or record.get("cuda_execution_allowed") is not False for record in records):
        errors.append("contract_allows_implementation_or_cuda_execution")


def _validate_kernel_abi(errors: list[str], records: list[dict[str, Any]]) -> None:
    if len(records) != 1:
        return
    record = records[0]
    if record.get("cuda_c_style_subset") is not True:
        errors.append("kernel_abi_not_cuda_c_style_subset")
    if record.get("cuda_kernel_implemented") is not False or record.get("cuda_source_modified") is not False:
        errors.append("kernel_abi_indicates_implementation")
    forbidden = set(record.get("forbidden_cuda_features", []))
    if not {"std::vector", "std::string", "exceptions", "dynamic_allocation"}.issubset(forbidden):
        errors.append("kernel_abi_missing_forbidden_features")


def _validate_host_runner(errors: list[str], records: list[dict[str, Any]]) -> None:
    if len(records) != 1:
        return
    record = records[0]
    if record.get("cuda_host_runner_implemented") is not False or record.get("cxx_launches_python_workers") is not False:
        errors.append("host_runner_contract_violation")


def _validate_buffer_contract(errors: list[str], records: list[dict[str, Any]]) -> None:
    names = {str(record.get("buffer_name")) for record in records}
    required = {"token_values", "transformable_mask", "fixture_offsets_lengths", "stream_schedule_values", "output_tokens", "status_codes", "output_hash_policy", "candidate_fixture_stream_refs"}
    missing = required - names
    if missing:
        errors.append(f"buffer_contract_missing_buffers: {sorted(missing)}")


def _validate_validation_vectors(errors: list[str], records: list[dict[str, Any]]) -> None:
    kinds = {str(record.get("validation_vector_kind")) for record in records}
    required = {
        "synthetic_positive",
        "bounded_p56_fixture_safe",
        "full_p56_blocker",
        "invalid_token_value_control",
        "invalid_stream_start_control",
        "separator_preservation_control",
        "zero_transformable_control",
    }
    if required - kinds:
        errors.append(f"validation_vectors_missing_kinds: {sorted(required - kinds)}")
    full = [record for record in records if record.get("validation_vector_kind") == "full_p56_blocker"]
    if len(full) != 1 or not str(full[0].get("validation_status", "")).startswith("blocked"):
        errors.append("full_p56_validation_vector_not_blocked")
    ready = [record for record in records if record.get("validation_vector_kind") in {"synthetic_positive", "bounded_p56_fixture_safe"}]
    if any(not record.get("expected_output_token_hash") for record in ready):
        errors.append("ready_validation_vector_missing_hash")


def _validate_future_parity(errors: list[str], records: list[dict[str, Any]]) -> None:
    if any(record.get("execution_enabled") is not False or record.get("cuda_execution_allowed") is not False for record in records):
        errors.append("future_parity_allows_execution")


def _validate_result_store(errors: list[str], records: list[dict[str, Any]]) -> None:
    contracts = {record.get("compatibility_contract") for record in records}
    if contracts != {"stage4p", "stage4i"}:
        errors.append(f"result_store_contracts_unexpected: {sorted(str(item) for item in contracts)}")
    if any(record.get("result_body_publication_allowed") is not False for record in records):
        errors.append("result_store_allows_body_publication")


def _validate_full_p56(errors: list[str], records: list[dict[str, Any]]) -> None:
    if len(records) != 1:
        return
    record = records[0]
    if record.get("blocker_status") != "enforced" or record.get("full_token_buffer_committed") is not False:
        errors.append("full_p56_blocker_not_enforced")


def _validate_scored(errors: list[str], records: list[dict[str, Any]]) -> None:
    if any(record.get("execution_enabled") is not False or record.get("benchmark_allowed") is not False for record in records):
        errors.append("scored_deferral_allows_execution")
    if not any(record.get("experiment_class") == "bounded_unsolved_page_micro_pilot" and str(record.get("readiness_status")).startswith("blocked") for record in records):
        errors.append("unsolved_scored_deferral_missing")


def _validate_gate(errors: list[str], records: list[dict[str, Any]]) -> None:
    if len(records) != 1:
        return
    record = records[0]
    if record.get("future_synthetic_kernel_implementation_ready") is not True:
        errors.append("future_synthetic_kernel_not_ready")
    if record.get("current_stage_allows_kernel_implementation") is not False:
        errors.append("implementation_gate_allows_current_kernel")


def _validate_decisions(errors: list[str], records: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    selected = [record for record in records if record.get("selected") is True]
    if len(selected) != 1:
        errors.append(f"selected_next_stage_count_mismatch: {len(selected)}")
        return
    if selected[0].get("option_id") != "stage5aa_prime_minus_one_cuda_synthetic_kernel_implementation":
        errors.append("selected_next_stage_unexpected")
    if "Stage 5AA - prime-minus-one CUDA synthetic kernel implementation and parity" not in str(summary.get("recommended_next_stage_title", "")):
        errors.append("summary_next_stage_unexpected")


def _validate_summary(errors: list[str], summary: dict[str, Any]) -> None:
    for key in BAD_TRUE_FLAGS:
        value = summary.get(key)
        if value is True or (key == "new_cuda_kernels_added" and value not in {0, False, None}):
            errors.append(f"summary_guardrail_violation: {key}={value}")
    if summary.get("status") != "complete" or summary.get("stage_id") != "stage-5z":
        errors.append("summary_stage_or_status_unexpected")
    if summary.get("future_synthetic_kernel_implementation_ready") is not True:
        errors.append("summary_future_synthetic_ready_not_true")


def _validate_reports(errors: list[str], results_dir: Path) -> None:
    resolved = resolve(results_dir)
    for filename in REPORT_FILES.values():
        if not (resolved / filename).exists():
            errors.append(f"missing_generated_report: {resolved / filename}")


__all__ = ["validate_stage5z_results"]
