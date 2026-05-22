"""Validation for Stage 5Y prime-minus-one native reporting records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_reporting.export import read_records, read_yaml, resolve
from libreprimus.prime_minus_one_native_reporting.models import BAD_TRUE_FLAGS, REPORT_FILES


def validate_stage5y_results(
    *,
    parity_report_path: Path,
    result_store_integration_path: Path,
    score_summary_integration_path: Path,
    method_status_impact_path: Path,
    generated_body_policy_path: Path,
    full_p56_blocker_preservation_path: Path,
    cuda_contract_readiness_gate_path: Path,
    scored_experiment_readiness_path: Path,
    guardrail_path: Path,
    next_stage_decision_path: Path,
    summary_path: Path,
    results_dir: Path,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    parity = _load_records(errors, parity_report_path)
    result_store = _load_records(errors, result_store_integration_path)
    score = _load_records(errors, score_summary_integration_path)
    method = _load_records(errors, method_status_impact_path)
    policy = _load_records(errors, generated_body_policy_path)
    blockers = _load_records(errors, full_p56_blocker_preservation_path)
    gate = _load_records(errors, cuda_contract_readiness_gate_path)
    scored = _load_records(errors, scored_experiment_readiness_path)
    guardrails = _load_records(errors, guardrail_path)
    decisions = _load_records(errors, next_stage_decision_path)
    try:
        summary = read_yaml(summary_path)
    except (OSError, ValueError) as exc:
        summary = {}
        errors.append(f"summary_load_failed: {exc}")
    counts = {
        "parity_report_records": len(parity),
        "result_store_integration_records": len(result_store),
        "score_summary_integration_records": len(score),
        "method_status_impact_records": len(method),
        "generated_body_policy_records": len(policy),
        "full_p56_blocker_preservation_records": len(blockers),
        "cuda_contract_readiness_gate_records": len(gate),
        "bounded_scored_experiment_readiness_records": len(scored),
        "guardrail_records": len(guardrails),
        "next_stage_decision_records": len(decisions),
        "ready_mapping_count": sum(1 for record in parity if record.get("hash_match") is True),
        "blocked_mapping_count": sum(1 for record in parity if record.get("blocked_in_stage5x") is True),
    }
    _validate_counts(errors, counts, summary if isinstance(summary, dict) else {})
    for group, records in (
        ("parity", parity),
        ("result_store", result_store),
        ("score", score),
        ("method", method),
        ("policy", policy),
        ("blockers", blockers),
        ("gate", gate),
        ("scored", scored),
        ("guardrails", guardrails),
        ("decisions", decisions),
    ):
        for index, record in enumerate(records):
            _check_guardrails(errors, group, index, record)
    _validate_parity(errors, parity)
    _validate_result_store(errors, result_store)
    _validate_score(errors, score)
    _validate_method_status(errors, method)
    _validate_policy(errors, policy)
    _validate_blockers(errors, blockers)
    _validate_gate(errors, gate)
    _validate_scored(errors, scored)
    _validate_decisions(errors, decisions, summary if isinstance(summary, dict) else {})
    _validate_reports(errors, results_dir)
    counts["stage5y_valid"] = not errors
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


def _validate_counts(errors: list[str], counts: dict[str, int], summary: dict[str, Any]) -> None:
    expected = {
        "parity_report_records": 3,
        "result_store_integration_records": 3,
        "score_summary_integration_records": 3,
        "method_status_impact_records": 5,
        "generated_body_policy_records": 7,
        "full_p56_blocker_preservation_records": 1,
        "cuda_contract_readiness_gate_records": 1,
        "bounded_scored_experiment_readiness_records": 6,
        "guardrail_records": 9,
        "next_stage_decision_records": 10,
    }
    summary_keys = {
        "parity_report_records": "native_parity_report_records",
        "result_store_integration_records": "result_store_integration_records",
        "score_summary_integration_records": "score_summary_integration_records",
        "method_status_impact_records": "method_status_impact_records",
        "generated_body_policy_records": "generated_body_policy_records",
        "full_p56_blocker_preservation_records": "full_p56_blocker_preservation_records",
        "cuda_contract_readiness_gate_records": "cuda_contract_readiness_gate_records",
        "bounded_scored_experiment_readiness_records": "bounded_scored_experiment_readiness_records",
        "guardrail_records": "guardrail_records",
        "next_stage_decision_records": "next_stage_decision_records",
    }
    for key, value in expected.items():
        if counts.get(key) != value:
            errors.append(f"{key}_count_mismatch: {counts.get(key)} != {value}")
        if summary.get(summary_keys[key]) != value:
            errors.append(f"{summary_keys[key]}_summary_mismatch: {summary.get(summary_keys[key])} != {value}")


def _validate_parity(errors: list[str], parity: list[dict[str, Any]]) -> None:
    if sum(1 for record in parity if record.get("hash_match") is True) != 2:
        errors.append("stage5x_hash_match_count_mismatch")
    blocked = [record for record in parity if record.get("mapping_id") == "stage5w-mapping-p56-full-fixture-blocked-v0"]
    if len(blocked) != 1 or blocked[0].get("blocked_in_stage5x") is not True:
        errors.append("full_p56_report_not_blocked")


def _validate_result_store(errors: list[str], records: list[dict[str, Any]]) -> None:
    for record in records:
        if record.get("result_store_contract") != "stage4p" or record.get("stage4p_compatibility") != "compatible":
            errors.append("result_store_not_stage4p_compatible")
        if record.get("generated_body_publication_allowed") is not False:
            errors.append("result_store_generated_body_publication_allowed")


def _validate_score(errors: list[str], records: list[dict[str, Any]]) -> None:
    for record in records:
        if record.get("score_summary_contract") != "stage4i" or record.get("confidence_interpretation") != "triage_only":
            errors.append("score_summary_not_stage4i_triage")
        if record.get("confidence_label") not in {"positive_control_like", "scoring_not_available"}:
            errors.append(f"score_summary_unknown_label: {record.get('confidence_label')}")


def _validate_method_status(errors: list[str], records: list[dict[str, Any]]) -> None:
    if any(record.get("marked_solved") is True or record.get("method_status_upgraded") is True for record in records):
        errors.append("method_status_upgrade_detected")


def _validate_policy(errors: list[str], records: list[dict[str, Any]]) -> None:
    if any(record.get("generated_body_publication_allowed") is not False for record in records):
        errors.append("generated_body_policy_allows_publication")


def _validate_blockers(errors: list[str], records: list[dict[str, Any]]) -> None:
    if len(records) != 1:
        errors.append(f"full_p56_blocker_preservation_count_mismatch: {len(records)}")
        return
    record = records[0]
    if record.get("blocker_status") != "enforced" or record.get("full_token_buffer_committed") is not False:
        errors.append("full_p56_blocker_not_enforced")
    if int(record.get("full_schedule_value_count", 0)) != 84:
        errors.append("full_p56_schedule_count_unexpected")


def _validate_gate(errors: list[str], records: list[dict[str, Any]]) -> None:
    if len(records) != 1:
        errors.append(f"cuda_contract_gate_count_mismatch: {len(records)}")
        return
    record = records[0]
    if record.get("prime_minus_one_cuda_contract_preparation_ready") is not True:
        errors.append("cuda_contract_preparation_not_ready")
    if record.get("cuda_execution_allowed") is not False or record.get("new_kernel_allowed") is not False:
        errors.append("cuda_contract_gate_allows_execution_or_kernel")


def _validate_scored(errors: list[str], records: list[dict[str, Any]]) -> None:
    by_class = {record.get("experiment_class"): record for record in records}
    if not str(by_class.get("bounded_cpu_native_prime_minus_one_scored_experiment", {}).get("readiness_status", "")).startswith("ready"):
        errors.append("cpu_native_scored_experiment_not_ready_for_manifest_gate")
    if not str(by_class.get("bounded_unsolved_page_micro_pilot", {}).get("readiness_status", "")).startswith("blocked"):
        errors.append("unsolved_page_micro_pilot_not_blocked")
    if any(record.get("benchmark_allowed") is True for record in records):
        errors.append("scored_readiness_allows_benchmark")


def _validate_decisions(errors: list[str], decisions: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    selected = [record for record in decisions if record.get("selected") is True]
    if len(selected) != 1:
        errors.append(f"selected_next_stage_count_mismatch: {len(selected)}")
    elif selected[0].get("option_id") != "stage5z_prime_minus_one_cuda_contract_preparation":
        errors.append("selected_next_stage_unexpected")
    if "Stage 5Z - prime-minus-one CUDA contract preparation" not in str(summary.get("recommended_next_stage_title", "")):
        errors.append("summary_next_stage_unexpected")


def _validate_reports(errors: list[str], results_dir: Path) -> None:
    resolved = resolve(results_dir)
    for filename in REPORT_FILES.values():
        if not (resolved / filename).exists():
            errors.append(f"missing_generated_report: {resolved / filename}")
