"""Build and read Stage 5S aggregate summaries."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_expanded_cuda_result_store.export import read_mapping, read_record_set, write_mapping, write_report
from libreprimus.gematria_expanded_cuda_result_store.models import (
    COMMON_FLAGS,
    NEXT_DEEP_RESEARCH_PROMPT,
    NEXT_DEEP_RESEARCH_REASON,
    SUMMARY_JSON,
    SUMMARY_PATH,
    OUTPUT_DIR,
    PARITY_REPORT_PATH,
    RESULT_STORE_INTEGRATION_PATH,
    SCORE_SUMMARY_INTEGRATION_PATH,
    METHOD_STATUS_IMPACT_PATH,
    GENERATED_BODY_POLICY_PATH,
    BOUNDARY_REVIEW_PATH,
    NEXT_STEP_DECISION_PATH,
    STAGE5R_SUMMARY,
)


def build_summary(
    *,
    parity_report: Path = PARITY_REPORT_PATH,
    result_store_integration: Path = RESULT_STORE_INTEGRATION_PATH,
    score_summary_integration: Path = SCORE_SUMMARY_INTEGRATION_PATH,
    method_status_impact: Path = METHOD_STATUS_IMPACT_PATH,
    generated_body_policy: Path = GENERATED_BODY_POLICY_PATH,
    boundary_review: Path = BOUNDARY_REVIEW_PATH,
    next_step_decision: Path = NEXT_STEP_DECISION_PATH,
    stage5r_summary: Path = STAGE5R_SUMMARY,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    parity = read_record_set(parity_report)
    result_store = read_record_set(result_store_integration)
    score = read_record_set(score_summary_integration)
    method = read_record_set(method_status_impact)
    policy = read_record_set(generated_body_policy)
    boundary = read_record_set(boundary_review)
    decisions = read_record_set(next_step_decision)
    source_summary = read_mapping(stage5r_summary)
    selected = next(record for record in decisions if record["selected"])
    payload = {
        "record_type": "stage5s_expanded_cuda_result_store_integration_summary",
        "schema": "schemas/cuda/stage5s-expanded-cuda-result-store-integration-summary-v0.schema.json",
        "status": "complete",
        "source_stage5r_records_consumed": len(parity),
        "parity_report_records": len(parity),
        "result_store_integration_records": len(result_store),
        "score_summary_integration_records": len(score),
        "method_status_impact_records": len(method),
        "generated_body_policy_records": len(policy),
        "boundary_review_records": len(boundary),
        "controlled_next_step_decision_records": len(decisions),
        "stage4p_compatibility": all(record["stage4p_compatibility"] for record in result_store),
        "stage4i_compatibility": all(record["scorer_contract"] == "stage4i" for record in score),
        "generated_body_publication_allowed": False,
        "method_status_upgrade_allowed": False,
        "selected_next_prompt": selected["selected_next_prompt"],
        "selected_next_stage_reason": selected["selected_next_stage_reason"],
        "deep_research_recommended": True,
        "deep_research_recommendation_reason": NEXT_DEEP_RESEARCH_REASON,
        "remaining_blockers": [],
        "newly_discovered_blockers": [],
        "source_stage5r_cuda_attempted_count": source_summary.get("cuda_attempted_count"),
        "source_stage5r_parity_pass_count": source_summary.get("parity_pass_count"),
        "codex_output_written": False,
    }
    payload.update(COMMON_FLAGS)
    payload["selected_next_prompt"] = NEXT_DEEP_RESEARCH_PROMPT
    write_mapping(summary_out, payload)
    write_report(out_dir, SUMMARY_JSON, payload)
    return payload


def load_summary(path: Path = SUMMARY_PATH) -> dict[str, Any]:
    return read_mapping(path)
