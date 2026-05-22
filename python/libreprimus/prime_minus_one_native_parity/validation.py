"""Validation for Stage 5X prime-minus-one native parity records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_parity.export import read_records, read_yaml, resolve
from libreprimus.prime_minus_one_native_parity.models import BAD_TRUE_FLAGS, REPORT_FILES


def validate_stage5x_results(
    *,
    native_run_path: Path,
    native_parity_path: Path,
    result_store_preflight_path: Path,
    score_summary_preflight_path: Path,
    full_p56_blocker_path: Path,
    guardrail_path: Path,
    next_stage_decision_path: Path,
    summary_path: Path,
    results_dir: Path,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    runs = _load_records(errors, native_run_path)
    parity = _load_records(errors, native_parity_path)
    result_store = _load_records(errors, result_store_preflight_path)
    score = _load_records(errors, score_summary_preflight_path)
    blockers = _load_records(errors, full_p56_blocker_path)
    guardrails = _load_records(errors, guardrail_path)
    decisions = _load_records(errors, next_stage_decision_path)
    try:
        summary = read_yaml(summary_path)
    except (OSError, ValueError) as exc:
        summary = {}
        errors.append(f"summary_load_failed: {exc}")
    counts = {
        "native_run_records": len(runs),
        "native_parity_records": len(parity),
        "result_store_preflight_records": len(result_store),
        "score_summary_preflight_records": len(score),
        "full_p56_blocker_records": len(blockers),
        "guardrail_records": len(guardrails),
        "next_stage_decision_records": len(decisions),
        "native_execution_attempted_count": sum(1 for record in runs if record.get("native_execution_performed") is True),
        "native_pass_count": sum(1 for record in parity if record.get("parity_status") == "passed"),
        "native_fail_count": sum(1 for record in parity if record.get("parity_status") == "failed_hash_mismatch"),
        "native_skip_count": sum(1 for record in runs if str(record.get("native_execution_status", "")).startswith("skipped")),
    }
    _validate_counts(errors, counts, summary if isinstance(summary, dict) else {})
    for group, records in (
        ("runs", runs),
        ("parity", parity),
        ("result_store", result_store),
        ("score", score),
        ("blockers", blockers),
        ("guardrails", guardrails),
        ("decisions", decisions),
    ):
        for index, record in enumerate(records):
            _check_guardrails(errors, group, index, record)
    _validate_parity(errors, runs, parity)
    _validate_blockers(errors, blockers)
    _validate_decisions(errors, decisions, summary if isinstance(summary, dict) else {})
    _validate_reports(errors, results_dir)
    counts["stage5x_valid"] = not errors
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
        "native_run_records": 3,
        "native_parity_records": 3,
        "result_store_preflight_records": 3,
        "score_summary_preflight_records": 3,
        "full_p56_blocker_records": 1,
        "native_execution_attempted_count": 2,
        "native_pass_count": 2,
        "native_fail_count": 0,
        "native_skip_count": 1,
    }
    for key, value in expected.items():
        if counts.get(key) != value:
            errors.append(f"{key}_count_mismatch: {counts.get(key)} != {value}")
        if summary.get(key) != value:
            errors.append(f"{key}_summary_mismatch: {summary.get(key)} != {value}")


def _validate_parity(errors: list[str], runs: list[dict[str, Any]], parity: list[dict[str, Any]]) -> None:
    ready = [record for record in runs if record.get("mapping_id") != "stage5w-mapping-p56-full-fixture-blocked-v0"]
    if len(ready) != 2:
        errors.append(f"ready_run_count_mismatch: {len(ready)}")
    for record in ready:
        if record.get("computed_output_token_hash") != record.get("expected_output_token_hash"):
            errors.append(f"{record.get('mapping_id')} hash_mismatch")
    blocked = [record for record in parity if record.get("mapping_id") == "stage5w-mapping-p56-full-fixture-blocked-v0"]
    if len(blocked) != 1 or blocked[0].get("parity_status") != "blocked_not_executed":
        errors.append("full_p56_not_blocked")


def _validate_blockers(errors: list[str], blockers: list[dict[str, Any]]) -> None:
    if len(blockers) != 1:
        errors.append(f"full_p56_blocker_count_mismatch: {len(blockers)}")
        return
    record = blockers[0]
    if record.get("full_token_buffer_committed") is not False or record.get("native_execution_allowed") is not False:
        errors.append("full_p56_blocker_policy_failed")
    if int(record.get("full_schedule_value_count", 0)) != 84:
        errors.append("full_p56_schedule_count_unexpected")


def _validate_decisions(errors: list[str], decisions: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    selected = [record for record in decisions if record.get("selected") is True]
    if len(selected) != 1:
        errors.append(f"selected_next_stage_count_mismatch: {len(selected)}")
    elif "Stage 5Y - prime-minus-one native parity reporting" not in str(selected[0].get("recommended_stage_title")):
        errors.append("selected_next_stage_unexpected")
    if summary.get("stage5y_ready") is not True:
        errors.append("summary_stage5y_ready_not_true")


def _validate_reports(errors: list[str], results_dir: Path) -> None:
    resolved = resolve(results_dir)
    for filename in REPORT_FILES.values():
        if not (resolved / filename).exists():
            errors.append(f"missing_generated_report: {resolved / filename}")
