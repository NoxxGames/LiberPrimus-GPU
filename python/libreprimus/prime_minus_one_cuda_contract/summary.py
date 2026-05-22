"""Build Stage 5Z prime-minus-one CUDA contract summary."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_cuda_contract.export import read_records, write_json_report, write_summary, write_warnings
from libreprimus.prime_minus_one_cuda_contract.models import (
    BUFFER_CONTRACT_PATH,
    COMMON_FALSE_FLAGS,
    COMMON_TRUE_FLAGS,
    CUDA_CONTRACT_PATH,
    EXPECTED_COUNTS,
    FULL_P56_BLOCKER_PATH,
    FUTURE_PARITY_PLAN_PATH,
    HOST_RUNNER_CONTRACT_PATH,
    IMPLEMENTATION_READINESS_PATH,
    KERNEL_ABI_PATH,
    NEXT_STAGE_DECISION_PATH,
    NEXT_STAGE_REASON,
    NEXT_STAGE_TITLE,
    OUTPUT_DIR,
    RESULT_STORE_COMPATIBILITY_PATH,
    SCORED_EXPERIMENT_DEFERRAL_PATH,
    SOURCE_NATIVE_CONTRACT_ID,
    SUMMARY_PATH,
    VALIDATION_VECTORS_PATH,
)


def build_summary(
    *,
    cuda_contract: Path = CUDA_CONTRACT_PATH,
    kernel_abi: Path = KERNEL_ABI_PATH,
    host_runner_contract: Path = HOST_RUNNER_CONTRACT_PATH,
    buffer_contract: Path = BUFFER_CONTRACT_PATH,
    validation_vectors: Path = VALIDATION_VECTORS_PATH,
    future_parity_plan: Path = FUTURE_PARITY_PLAN_PATH,
    result_store_compatibility: Path = RESULT_STORE_COMPATIBILITY_PATH,
    full_p56_blocker: Path = FULL_P56_BLOCKER_PATH,
    scored_experiment_deferral: Path = SCORED_EXPERIMENT_DEFERRAL_PATH,
    implementation_readiness_gate: Path = IMPLEMENTATION_READINESS_PATH,
    next_stage_decision: Path = NEXT_STAGE_DECISION_PATH,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    contract_records = read_records(cuda_contract)
    kernel_records = read_records(kernel_abi)
    host_records = read_records(host_runner_contract)
    buffer_records = read_records(buffer_contract)
    vector_records = read_records(validation_vectors)
    parity_plan_records = read_records(future_parity_plan)
    result_store_records = read_records(result_store_compatibility)
    blocker_records = read_records(full_p56_blocker)
    scored_records = read_records(scored_experiment_deferral)
    gate_records = read_records(implementation_readiness_gate)
    decision_records = read_records(next_stage_decision)
    selected = next(record for record in decision_records if record.get("selected") is True)
    summary = {
        "record_type": "stage5z_prime_minus_one_cuda_contract_summary",
        "schema": "schemas/cuda/stage5z-prime-minus-one-cuda-contract-summary-v0.schema.json",
        "stage_id": "stage-5z",
        "status": "complete",
        "source_stage_id": "stage-5y",
        "candidate_batch_abi_id": "candidate_batch_abi_v0",
        "source_native_contract_id": SOURCE_NATIVE_CONTRACT_ID,
        "cuda_contract_records": len(contract_records),
        "kernel_abi_records": len(kernel_records),
        "host_runner_contract_records": len(host_records),
        "buffer_contract_records": len(buffer_records),
        "validation_vector_records": len(vector_records),
        "future_parity_plan_records": len(parity_plan_records),
        "result_store_compatibility_records": len(result_store_records),
        "full_p56_blocker_records": len(blocker_records),
        "scored_experiment_deferral_records": len(scored_records),
        "implementation_readiness_gate_records": len(gate_records),
        "next_stage_decision_records": len(decision_records),
        "expected_record_counts": EXPECTED_COUNTS,
        "contract_status": "ready_for_synthetic_cuda_kernel_implementation_contract_only",
        "implementation_readiness_status": gate_records[0].get("readiness_status") if gate_records else "missing",
        "full_p56_blocker_status": blocker_records[0].get("full_p56_status") if blocker_records else "missing",
        "scored_experiment_deferral_status": "deferred_manifest_gate_required",
        "selected_next_prompt": selected.get("recommended_stage_title"),
        "selected_next_prompt_reason": selected.get("rationale", NEXT_STAGE_REASON),
        "deep_research_recommended_next": selected.get("recommended_prompt_type") == "Deep Research",
        "deep_research_recommended_next_reason": "Codex synthetic-only kernel implementation is selected before Deep Research.",
        "prime_minus_one_cuda_contract_preparation_complete": True,
        "future_synthetic_kernel_implementation_ready": True,
        "bounded_scored_experiment_deferred": True,
        "recommended_next_stage_title": selected.get("recommended_stage_title", NEXT_STAGE_TITLE),
        "recommended_next_stage_reason": selected.get("rationale", NEXT_STAGE_REASON),
        "recommended_next_prompt_type": selected.get("recommended_prompt_type", "Codex"),
        **COMMON_TRUE_FLAGS,
        **COMMON_FALSE_FLAGS,
    }
    write_summary(summary_out, summary)
    write_json_report(out_dir, "summary.json", summary)
    write_warnings(out_dir, [])
    return summary


__all__ = ["build_summary"]
