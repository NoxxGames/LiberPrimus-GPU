"""Validation for Stage 5V native Candidate Batch ABI conformance records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import resolve_repo_path
from libreprimus.native_candidate_batch_conformance.export import read_mapping, read_record_set
from libreprimus.native_candidate_batch_conformance.models import BAD_TRUE_FLAGS, EXPECTED_COUNTS, REPORT_FILES


def validate_stage5v_results(
    *,
    adapter_records_path: Path,
    conformance_fixtures_path: Path,
    token_buffer_conformance_path: Path,
    schedule_conformance_path: Path,
    score_vector_conformance_path: Path,
    topk_conformance_path: Path,
    result_store_conformance_path: Path,
    implementation_status_path: Path,
    next_stage_decision_path: Path,
    summary_path: Path,
    results_dir: Path,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    adapter = _load_records(errors, adapter_records_path)
    fixtures = _load_records(errors, conformance_fixtures_path)
    token = _load_records(errors, token_buffer_conformance_path)
    schedule = _load_records(errors, schedule_conformance_path)
    score = _load_records(errors, score_vector_conformance_path)
    topk = _load_records(errors, topk_conformance_path)
    result_store = _load_records(errors, result_store_conformance_path)
    status = _load_records(errors, implementation_status_path)
    decisions = _load_records(errors, next_stage_decision_path)
    try:
        summary = read_mapping(summary_path)
    except (OSError, ValueError) as exc:
        errors.append(f"summary_load_failed: {exc}")
        summary = {}

    counts = {
        "native_adapter_records": len(adapter),
        "conformance_fixture_records": len(fixtures),
        "token_buffer_conformance_records": len(token),
        "schedule_conformance_records": len(schedule),
        "score_vector_conformance_records": len(score),
        "topk_conformance_records": len(topk),
        "result_store_conformance_records": len(result_store),
        "abi_implementation_status_records": len(status),
        "next_stage_decision_records": len(decisions),
        "executed_conformance_fixture_count": sum(
            1 for record in fixtures if record.get("execution_status") == "executed_python_reference"
        ),
        "output_hash_records": sum(1 for record in fixtures if record.get("expected_output_token_hash")),
    }
    for key, expected in EXPECTED_COUNTS.items():
        if key in counts and counts[key] != expected:
            errors.append(f"{key}_count_mismatch: {counts[key]} != {expected}")
        if key in summary and summary[key] != expected:
            errors.append(f"{key}_summary_mismatch: {summary[key]} != {expected}")

    for group_name, records in (
        ("adapter", adapter),
        ("fixtures", fixtures),
        ("token", token),
        ("schedule", schedule),
        ("score", score),
        ("topk", topk),
        ("result_store", result_store),
        ("status", status),
        ("decisions", decisions),
    ):
        for index, record in enumerate(records):
            _check_guardrails(errors, group_name, index, record)

    for record in fixtures:
        _validate_fixture(errors, record)
    selected = [record for record in decisions if record.get("selected") is True]
    if len(selected) != 1:
        errors.append(f"selected_next_stage_count_mismatch: {len(selected)}")
    elif "prime-minus-one stream native parity contract" not in str(selected[0].get("recommended_stage_title", "")).lower():
        errors.append("selected_next_stage_unexpected")
    if summary.get("solve_claim") is not False or summary.get("no_solve_claim") is not True:
        errors.append("summary_solve_claim_guardrail_failed")
    if summary.get("cuda_execution_performed") is not False:
        errors.append("summary_cuda_execution_guardrail_failed")
    if summary.get("python_reference_adapter_implemented") is not True:
        errors.append("summary_python_adapter_missing")
    if summary.get("cpp_reference_adapter_implemented") is not False:
        errors.append("summary_cpp_adapter_should_be_false")

    resolved_results = resolve_repo_path(results_dir)
    for filename in REPORT_FILES.values():
        path = resolved_results / filename
        if not path.exists():
            errors.append(f"missing_generated_report: {path}")
    counts["stage5v_valid"] = not errors
    return counts, errors


def _load_records(errors: list[str], path: Path) -> list[dict[str, Any]]:
    try:
        return read_record_set(path)
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


def _validate_fixture(errors: list[str], record: dict[str, Any]) -> None:
    tokens = list(record.get("token_values", []))
    mask = list(record.get("transformable_mask", []))
    kinds = list(record.get("token_kind", []))
    separators = {int(item) for item in record.get("separator_positions", [])}
    if len(mask) != len(tokens):
        errors.append(f"{record.get('fixture_id')} mask_length_mismatch")
    if len(kinds) != len(tokens):
        errors.append(f"{record.get('fixture_id')} token_kind_length_mismatch")
    for index, token in enumerate(tokens):
        if index in separators and mask[index] is not False:
            errors.append(f"{record.get('fixture_id')} separator_transformable")
        if token != -1 and not 0 <= int(token) <= 28:
            errors.append(f"{record.get('fixture_id')} token_out_of_domain")
    for offset, length in zip(record.get("fixture_offsets", []), record.get("fixture_lengths", []), strict=True):
        if int(offset) < 0 or int(length) < 1 or int(offset) + int(length) > len(tokens):
            errors.append(f"{record.get('fixture_id')} invalid_offset_length")
