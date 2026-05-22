"""Validation for Stage 5W prime-minus-one native contract records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_contract.export import read_records, read_yaml, resolve
from libreprimus.prime_minus_one_native_contract.models import BAD_TRUE_FLAGS, EXPECTED_COUNTS, REPORT_FILES


def validate_stage5w_results(
    *,
    source_inventory_path: Path,
    stream_contract_path: Path,
    prime_schedule_path: Path,
    candidate_batch_mapping_path: Path,
    native_parity_preparation_path: Path,
    result_store_preflight_path: Path,
    guardrail_path: Path,
    next_stage_decision_path: Path,
    summary_path: Path,
    results_dir: Path,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    source = _load_records(errors, source_inventory_path)
    contract = _load_records(errors, stream_contract_path)
    schedule = _load_records(errors, prime_schedule_path)
    mapping = _load_records(errors, candidate_batch_mapping_path)
    prep = _load_records(errors, native_parity_preparation_path)
    result = _load_records(errors, result_store_preflight_path)
    guardrail = _load_records(errors, guardrail_path)
    decisions = _load_records(errors, next_stage_decision_path)
    try:
        summary = read_yaml(summary_path)
    except (OSError, ValueError) as exc:
        summary = {}
        errors.append(f"summary_load_failed: {exc}")
    counts: dict[str, Any] = {
        "source_inventory_records": len(source),
        "stream_contract_records": len(contract),
        "prime_schedule_records": len(schedule),
        "candidate_batch_mapping_records": len(mapping),
        "native_parity_preparation_records": len(prep),
        "result_store_preflight_records": len(result),
        "guardrail_records": len(guardrail),
        "next_stage_decision_records": len(decisions),
        "synthetic_control_schedule_records": sum(1 for record in schedule if str(record.get("schedule_status")).startswith("synthetic")),
        "synthetic_control_ready_count": sum(1 for record in mapping if record.get("mapping_status") == "synthetic_control_ready"),
    }
    for key, expected in EXPECTED_COUNTS.items():
        if counts.get(key) != expected:
            errors.append(f"{key}_count_mismatch: {counts.get(key)} != {expected}")
        if isinstance(summary, dict) and summary.get(key) != expected:
            errors.append(f"{key}_summary_mismatch: {summary.get(key)} != {expected}")
    for group_name, records in (
        ("source", source),
        ("contract", contract),
        ("schedule", schedule),
        ("mapping", mapping),
        ("prep", prep),
        ("result", result),
        ("guardrail", guardrail),
        ("decisions", decisions),
    ):
        for index, record in enumerate(records):
            _check_guardrails(errors, group_name, index, record)
    _validate_prime_schedules(errors, schedule)
    _validate_decisions(errors, decisions)
    _validate_summary(errors, summary if isinstance(summary, dict) else {})
    resolved_results = resolve(results_dir)
    for filename in REPORT_FILES.values():
        if not (resolved_results / filename).exists():
            errors.append(f"missing_generated_report: {resolved_results / filename}")
    counts["stage5w_valid"] = not errors
    return counts, errors


def _load_records(errors: list[str], path: Path) -> list[dict[str, Any]]:
    try:
        return read_records(path)
    except (OSError, ValueError) as exc:
        errors.append(f"record_load_failed: {path}: {exc}")
        return []


def _check_guardrails(errors: list[str], group: str, index: int, record: dict[str, Any]) -> None:
    for key in BAD_TRUE_FLAGS:
        if record.get(key) is True:
            errors.append(f"{group}[{index}] guardrail_true: {key}")
    if record.get("no_solve_claim") is not True:
        errors.append(f"{group}[{index}] no_solve_claim_not_true")
    if record.get("no_gpu_ci_safe") is not True:
        errors.append(f"{group}[{index}] no_gpu_ci_safe_not_true")


def _validate_prime_schedules(errors: list[str], records: list[dict[str, Any]]) -> None:
    for record in records:
        primes = [int(item) for item in record.get("first_n_primes", [])]
        values = [int(item) for item in record.get("stream_values_mod29", [])]
        if len(primes) != int(record.get("value_count", -1)) or len(values) != int(record.get("value_count", -1)):
            errors.append(f"{record.get('schedule_id')} value_count_mismatch")
        expected = [(prime - 1) % 29 for prime in primes]
        if values != expected:
            errors.append(f"{record.get('schedule_id')} stream_value_formula_mismatch")
        if record.get("prime_index_base") != 0:
            errors.append(f"{record.get('schedule_id')} prime_index_base_not_zero")


def _validate_decisions(errors: list[str], records: list[dict[str, Any]]) -> None:
    selected = [record for record in records if record.get("selected") is True]
    if len(selected) != 1:
        errors.append(f"selected_next_stage_count_mismatch: {len(selected)}")
    elif "no-GPU native parity execution" not in str(selected[0].get("recommended_stage_title")):
        errors.append("selected_next_stage_unexpected")


def _validate_summary(errors: list[str], summary: dict[str, Any]) -> None:
    if summary.get("record_type") != "stage5w_prime_minus_one_native_contract_summary":
        errors.append("summary_record_type_unexpected")
    for key in BAD_TRUE_FLAGS:
        if summary.get(key) is True:
            errors.append(f"summary_guardrail_true: {key}")
    if summary.get("p56_formula_direction_available") is not True:
        errors.append("summary_formula_direction_not_available")
    if summary.get("p56_skip_policy_available") is not True:
        errors.append("summary_skip_policy_not_available")
    if summary.get("solve_claim") is not False or summary.get("no_solve_claim") is not True:
        errors.append("summary_solve_claim_guardrail_failed")
