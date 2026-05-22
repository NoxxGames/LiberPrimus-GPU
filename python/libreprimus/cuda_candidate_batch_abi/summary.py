"""Build and load Stage 5U aggregate summaries."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_candidate_batch_abi.export import read_mapping, read_record_set, write_mapping, write_report, write_warnings
from libreprimus.cuda_candidate_batch_abi.models import (
    ABI_GAP_CLOSURE_PATH,
    BACKEND_SURFACE_CONTRACT_PATH,
    CANDIDATE_BATCH_ABI_PATH,
    COMMON_FLAGS,
    KEY_SCHEDULE_CONTRACT_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    RESULT_STORE_COMPATIBILITY_PATH,
    SCORE_VECTOR_CONTRACT_PATH,
    STAGE5T_GAPS,
    STAGE5T_SUMMARY,
    STREAM_SCHEDULE_CONTRACT_PATH,
    SUMMARY_JSON,
    SUMMARY_PATH,
    TOKEN_BUFFER_CONTRACT_PATH,
    TOPK_OUTPUT_CONTRACT_PATH,
    TRANSFORM_PARAMETER_CONTRACT_PATH,
)


def build_summary(
    *,
    candidate_batch_abi: Path = CANDIDATE_BATCH_ABI_PATH,
    token_buffer_contract: Path = TOKEN_BUFFER_CONTRACT_PATH,
    transform_parameter_contract: Path = TRANSFORM_PARAMETER_CONTRACT_PATH,
    key_schedule_contract: Path = KEY_SCHEDULE_CONTRACT_PATH,
    stream_schedule_contract: Path = STREAM_SCHEDULE_CONTRACT_PATH,
    score_vector_contract: Path = SCORE_VECTOR_CONTRACT_PATH,
    topk_output_contract: Path = TOPK_OUTPUT_CONTRACT_PATH,
    backend_surface_contract: Path = BACKEND_SURFACE_CONTRACT_PATH,
    result_store_compatibility: Path = RESULT_STORE_COMPATIBILITY_PATH,
    gap_closure: Path = ABI_GAP_CLOSURE_PATH,
    next_stage_decision: Path = NEXT_STAGE_DECISION_PATH,
    stage5t_gaps: Path = STAGE5T_GAPS,
    stage5t_summary: Path = STAGE5T_SUMMARY,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    """Build the committed Stage 5U aggregate summary."""

    abi = read_record_set(candidate_batch_abi)
    token = read_record_set(token_buffer_contract)
    transform = read_record_set(transform_parameter_contract)
    key = read_record_set(key_schedule_contract)
    stream = read_record_set(stream_schedule_contract)
    score = read_record_set(score_vector_contract)
    topk = read_record_set(topk_output_contract)
    backend = read_record_set(backend_surface_contract)
    result_store = read_record_set(result_store_compatibility)
    closures = read_record_set(gap_closure)
    decisions = read_record_set(next_stage_decision)
    stage5t_gap_records = read_record_set(stage5t_gaps)
    stage5t = read_mapping(stage5t_summary)
    selected = next(record for record in decisions if record.get("selected"))
    payload = {
        "record_type": "stage5u_candidate_batch_abi_summary",
        "schema": "schemas/cuda/stage5u-candidate-batch-abi-summary-v0.schema.json",
        "stage_id": "stage-5u",
        "status": "complete",
        "source_stage_id": "stage-5t",
        "candidate_batch_abi_records": len(abi),
        "token_buffer_contract_records": len(token),
        "transform_parameter_contract_records": len(transform),
        "key_schedule_contract_records": len(key),
        "stream_schedule_contract_records": len(stream),
        "score_vector_contract_records": len(score),
        "topk_output_contract_records": len(topk),
        "backend_surface_contract_records": len(backend),
        "result_store_compatibility_records": len(result_store),
        "abi_gap_closure_records": len(closures),
        "next_stage_decision_records": len(decisions),
        "stage5t_gap_count": len(stage5t_gap_records),
        "stage5t_gaps_closed_by_contract_count": sum(1 for record in closures if record["stage5u_closure_status"] == "closed_by_contract"),
        "stage5t_gaps_partially_closed_count": sum(1 for record in closures if record["stage5u_closure_status"].startswith("partially_closed")),
        "stage5t_gaps_still_blocked_count": sum(1 for record in closures if record["stage5u_closure_status"].startswith("still_blocked")),
        "stage5t_implementation_pending_count": sum(1 for record in closures if record.get("implementation_pending")),
        "candidate_batch_abi_version": 0,
        "stage5t_selected_next_stage": stage5t.get("recommended_next_stage_title", ""),
        "recommended_next_prompt_type": selected["recommended_prompt_type"],
        "recommended_next_stage_title": selected["recommended_stage_title"],
        "recommended_next_stage_reason": selected["rationale"],
        "deep_research_recommended_next": selected["deep_research_recommended_next"],
        "codex_output_written": False,
    }
    payload.update(COMMON_FLAGS)
    write_mapping(summary_out, payload)
    write_report(out_dir, SUMMARY_JSON, payload)
    write_warnings(out_dir, [])
    return payload


def load_summary(path: Path = SUMMARY_PATH) -> dict[str, Any]:
    return read_mapping(path)
