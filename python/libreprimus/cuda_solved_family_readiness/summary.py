"""Build and read Stage 5T aggregate summaries."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_solved_family_readiness.export import read_mapping, read_record_set, write_mapping, write_report
from libreprimus.cuda_solved_family_readiness.models import (
    BATCH_ABI_GAPS_PATH,
    BENCHMARK_READINESS_PATH,
    COMMON_FLAGS,
    INVENTORY_PATH,
    KERNEL_READINESS_PATH,
    NEXT_STAGE_DECISION_PATH,
    NO_UNSOLVED_GUARDRAIL_PATH,
    OUTPUT_DIR,
    PARITY_MATRIX_PATH,
    STAGE5S_SUMMARY,
    SUMMARY_JSON,
    SUMMARY_PATH,
)


def build_summary(
    *,
    solved_family_inventory: Path = INVENTORY_PATH,
    parity_matrix: Path = PARITY_MATRIX_PATH,
    kernel_readiness: Path = KERNEL_READINESS_PATH,
    batch_abi_gaps: Path = BATCH_ABI_GAPS_PATH,
    benchmark_readiness: Path = BENCHMARK_READINESS_PATH,
    no_unsolved_guardrail: Path = NO_UNSOLVED_GUARDRAIL_PATH,
    next_stage_decision: Path = NEXT_STAGE_DECISION_PATH,
    stage5s_summary: Path = STAGE5S_SUMMARY,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    inventory = read_record_set(solved_family_inventory)
    matrix = read_record_set(parity_matrix)
    kernels = read_record_set(kernel_readiness)
    abi_gaps = read_record_set(batch_abi_gaps)
    benchmarks = read_record_set(benchmark_readiness)
    guardrails = read_record_set(no_unsolved_guardrail)
    decisions = read_record_set(next_stage_decision)
    stage5s = read_mapping(stage5s_summary)
    selected = next(record for record in decisions if record.get("selected"))
    payload = {
        "record_type": "stage5t_cuda_solved_family_readiness_summary",
        "schema": "schemas/cuda/stage5t-cuda-solved-family-readiness-summary-v0.schema.json",
        "stage_id": "stage-5t",
        "status": "complete",
        "source_stage_id": "stage-5s",
        "deep_research_review_consumed": True,
        "solved_family_inventory_records": len(inventory),
        "cuda_parity_matrix_records": len(matrix),
        "kernel_readiness_records": len(kernels),
        "batch_abi_gap_records": len(abi_gaps),
        "benchmark_readiness_records": len(benchmarks),
        "no_unsolved_guardrail_records": len(guardrails),
        "next_stage_decision_records": len(decisions),
        "verified_existing_cuda_parity_count": sum(
            1 for record in matrix if record["readiness_status"] == "cuda_parity_verified_existing_kernel"
        ),
        "ready_for_contract_review_count": sum(
            1 for record in kernels if record["readiness_status"] in {"ready_for_contract_review_after_abi", "needs_cuda_kernel_contract"}
        ),
        "needs_batch_abi_count": sum(1 for record in abi_gaps if record.get("blocking")),
        "blocked_original_transform_contract_count": sum(
            1 for record in matrix if record["readiness_status"] == "blocked_original_transform_contract"
        ),
        "blocked_unsolved_count": sum(1 for record in guardrails if record["guardrail_id"] == "unsolved_page_cuda"),
        "recommended_next_prompt_type": selected["recommended_prompt_type"],
        "recommended_next_stage_title": selected["recommended_stage_title"],
        "recommended_next_stage_reason": selected["rationale"],
        "deep_research_recommended_next": selected["deep_research_recommended_next"],
        "source_stage5s_records_consumed": stage5s.get("parity_report_records", 0),
        "codex_output_written": False,
    }
    payload.update(COMMON_FLAGS)
    write_mapping(summary_out, payload)
    write_report(out_dir, SUMMARY_JSON, payload)
    return payload


def load_summary(path: Path = SUMMARY_PATH) -> dict[str, Any]:
    return read_mapping(path)
