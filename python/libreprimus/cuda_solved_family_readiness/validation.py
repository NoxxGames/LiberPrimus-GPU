"""Validate Stage 5T CUDA solved-family readiness records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_solved_family_readiness.export import read_mapping, read_record_set, read_report
from libreprimus.cuda_solved_family_readiness.models import (
    BAD_TRUE_FLAGS,
    BATCH_ABI_GAPS_PATH,
    BENCHMARK_READINESS_PATH,
    INVENTORY_PATH,
    KERNEL_READINESS_PATH,
    NEXT_STAGE_DECISION_PATH,
    NO_UNSOLVED_GUARDRAIL_PATH,
    OUTPUT_DIR,
    PARITY_MATRIX_PATH,
    SUMMARY_JSON,
    SUMMARY_PATH,
)


def validate_stage5t_results(
    *,
    solved_family_inventory_path: Path = INVENTORY_PATH,
    parity_matrix_path: Path = PARITY_MATRIX_PATH,
    kernel_readiness_path: Path = KERNEL_READINESS_PATH,
    batch_abi_gaps_path: Path = BATCH_ABI_GAPS_PATH,
    benchmark_readiness_path: Path = BENCHMARK_READINESS_PATH,
    no_unsolved_guardrail_path: Path = NO_UNSOLVED_GUARDRAIL_PATH,
    next_stage_decision_path: Path = NEXT_STAGE_DECISION_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, int | bool | str], list[str]]:
    inventory = read_record_set(solved_family_inventory_path)
    matrix = read_record_set(parity_matrix_path)
    kernels = read_record_set(kernel_readiness_path)
    abi_gaps = read_record_set(batch_abi_gaps_path)
    benchmarks = read_record_set(benchmark_readiness_path)
    guardrails = read_record_set(no_unsolved_guardrail_path)
    decisions = read_record_set(next_stage_decision_path)
    summary = read_mapping(summary_path)
    errors: list[str] = []
    expected = {
        "solved_family_inventory_records": 8,
        "cuda_parity_matrix_records": 8,
        "kernel_readiness_records": 7,
        "batch_abi_gap_records": 5,
        "benchmark_readiness_records": 3,
        "no_unsolved_guardrail_records": 6,
        "next_stage_decision_records": 5,
    }
    actual = {
        "solved_family_inventory_records": len(inventory),
        "cuda_parity_matrix_records": len(matrix),
        "kernel_readiness_records": len(kernels),
        "batch_abi_gap_records": len(abi_gaps),
        "benchmark_readiness_records": len(benchmarks),
        "no_unsolved_guardrail_records": len(guardrails),
        "next_stage_decision_records": len(decisions),
    }
    for key, value in expected.items():
        if actual[key] != value:
            errors.append(f"{key}={actual[key]} expected {value}")
    _validate_common_flags([*inventory, *matrix, *kernels, *abi_gaps, *benchmarks, *guardrails, *decisions, summary], errors)
    family_ids = {record["solved_family_id"] for record in inventory}
    required_families = {
        "direct_translation",
        "reverse_gematria",
        "rotated_reverse_gematria",
        "vigenere_explicit_key",
        "prime_minus_one_stream",
        "gematria_shift_score_only",
        "synthetic_shift_score",
        "synthetic_gematria_mod29",
    }
    missing = sorted(required_families - family_ids)
    if missing:
        errors.append(f"missing_solved_families={missing}")
    direct = _find(matrix, "solved_family_id", "direct_translation")
    if direct is None or direct.get("original_transform_semantics_cuda_verified") is not False:
        errors.append("direct_translation_original_semantics_must_not_be_cuda_verified")
    for family in ("reverse_gematria", "rotated_reverse_gematria", "vigenere_explicit_key", "prime_minus_one_stream"):
        row = _find(matrix, "solved_family_id", family)
        if row is None or row.get("original_transform_semantics_cuda_verified") is not False:
            errors.append(f"{family}_original_semantics_must_not_be_cuda_verified")
    if not any(record["candidate_family_id"] == "prime_minus_one_stream" and record["requires_batch_abi"] for record in kernels):
        errors.append("prime_minus_one_requires_batch_abi")
    if not any(record["candidate_family_id"] == "vigenere_explicit_key" and record["requires_batch_abi"] for record in kernels):
        errors.append("vigenere_requires_batch_abi")
    if any(record.get("implementation_allowed_now") for record in kernels):
        errors.append("kernel_readiness_must_not_authorize_implementation")
    if any(record.get("benchmark_execution_allowed") for record in benchmarks):
        errors.append("benchmark_execution_must_remain_blocked")
    if not any(record["guardrail_id"] == "unsolved_page_cuda" and not record["allowed"] for record in guardrails):
        errors.append("unsolved_page_cuda_guardrail_missing")
    selected = [record for record in decisions if record.get("selected")]
    if len(selected) != 1:
        errors.append("exactly_one_next_stage_decision_must_be_selected")
    elif selected[0].get("recommended_stage_title") != "Stage 5U - unified candidate batch ABI and backend contract consolidation":
        errors.append("unexpected_next_stage_decision")
    try:
        read_report(results_dir, SUMMARY_JSON)
    except FileNotFoundError:
        errors.append("missing_ignored_stage5t_summary_report")
    counts: dict[str, int | bool | str] = {
        **actual,
        "verified_existing_cuda_parity_count": summary.get("verified_existing_cuda_parity_count", 0),
        "ready_for_contract_review_count": summary.get("ready_for_contract_review_count", 0),
        "needs_batch_abi_count": summary.get("needs_batch_abi_count", 0),
        "recommended_next_stage_title": str(summary.get("recommended_next_stage_title", "")),
        "deep_research_recommended_next": summary.get("deep_research_recommended_next") is True,
    }
    return counts, errors


def _validate_common_flags(records: list[dict[str, Any]], errors: list[str]) -> None:
    for record in records:
        label = str(record.get("record_type", "summary"))
        for flag in BAD_TRUE_FLAGS:
            if record.get(flag) is True:
                errors.append(f"{label} has forbidden true flag {flag}")
        if record.get("no_solve_claim") is not True:
            errors.append(f"{label} missing no_solve_claim=true")


def _find(records: list[dict[str, Any]], key: str, value: str) -> dict[str, Any] | None:
    return next((record for record in records if record.get(key) == value), None)
