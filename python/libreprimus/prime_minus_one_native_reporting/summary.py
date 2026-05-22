"""Build Stage 5Y prime-minus-one native reporting summary records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_reporting.export import read_records, read_yaml, write_json_report, write_summary
from libreprimus.prime_minus_one_native_reporting.models import (
    ABI_ID,
    COMMON_FALSE_FLAGS,
    COMMON_TRUE_FLAGS,
    CONTRACT_ID,
    CUDA_CONTRACT_READINESS_PATH,
    FULL_P56_BLOCKER_PRESERVATION_PATH,
    GENERATED_BODY_POLICY_PATH,
    GUARDRAIL_PATH,
    METHOD_STATUS_IMPACT_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    PARITY_REPORT_PATH,
    REPORT_FILES,
    RESULT_STORE_INTEGRATION_PATH,
    SCORE_SUMMARY_INTEGRATION_PATH,
    SCORED_EXPERIMENT_READINESS_PATH,
    SOURCE_STAGE_ID,
    STAGE5X_SUMMARY_PATH,
    STAGE_ID,
    SUMMARY_PATH,
)


def build_summary(
    *,
    parity_report: Path = PARITY_REPORT_PATH,
    result_store_integration: Path = RESULT_STORE_INTEGRATION_PATH,
    score_summary_integration: Path = SCORE_SUMMARY_INTEGRATION_PATH,
    method_status_impact: Path = METHOD_STATUS_IMPACT_PATH,
    generated_body_policy: Path = GENERATED_BODY_POLICY_PATH,
    full_p56_blocker_preservation: Path = FULL_P56_BLOCKER_PRESERVATION_PATH,
    cuda_contract_readiness_gate: Path = CUDA_CONTRACT_READINESS_PATH,
    scored_experiment_readiness: Path = SCORED_EXPERIMENT_READINESS_PATH,
    guardrail: Path = GUARDRAIL_PATH,
    next_stage_decision: Path = NEXT_STAGE_DECISION_PATH,
    stage5x_summary: Path = STAGE5X_SUMMARY_PATH,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    parity = read_records(parity_report)
    result_store = read_records(result_store_integration)
    score = read_records(score_summary_integration)
    method = read_records(method_status_impact)
    policy = read_records(generated_body_policy)
    blockers = read_records(full_p56_blocker_preservation)
    gate = read_records(cuda_contract_readiness_gate)
    scored = read_records(scored_experiment_readiness)
    guardrails = read_records(guardrail)
    decisions = read_records(next_stage_decision)
    source_summary = read_yaml(stage5x_summary)
    selected = next(record for record in decisions if record.get("selected") is True)
    cpu_native_ready = any(
        record.get("experiment_class") == "bounded_cpu_native_prime_minus_one_scored_experiment"
        and str(record.get("readiness_status")).startswith("ready")
        for record in scored
    )
    unsolved_ready = any(
        record.get("experiment_class") == "bounded_unsolved_page_micro_pilot"
        and str(record.get("readiness_status")).startswith("ready")
        for record in scored
    )
    summary = {
        "record_type": "stage5y_prime_minus_one_native_reporting_summary",
        "schema": "schemas/cuda/stage5y-prime-minus-one-native-reporting-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "status": "complete",
        "source_stage_id": SOURCE_STAGE_ID,
        "candidate_batch_abi_id": ABI_ID,
        "contract_id": CONTRACT_ID,
        "native_parity_report_records": len(parity),
        "result_store_integration_records": len(result_store),
        "score_summary_integration_records": len(score),
        "method_status_impact_records": len(method),
        "generated_body_policy_records": len(policy),
        "full_p56_blocker_preservation_records": len(blockers),
        "cuda_contract_readiness_gate_records": len(gate),
        "bounded_scored_experiment_readiness_records": len(scored),
        "guardrail_records": len(guardrails),
        "next_stage_decision_records": len(decisions),
        "source_stage5x_ready_mapping_count": source_summary.get("ready_mapping_count"),
        "source_stage5x_blocked_mapping_count": source_summary.get("blocked_mapping_count"),
        "source_stage5x_native_pass_count": source_summary.get("native_pass_count"),
        "source_stage5x_native_fail_count": source_summary.get("native_fail_count"),
        "source_stage5x_native_skip_count": source_summary.get("native_skip_count"),
        "stage5x_expected_hash_match_count": source_summary.get("stage5w_expected_hash_match_count"),
        "full_p56_status": "blocked_full_p56_token_buffer_missing",
        "prime_minus_one_cuda_contract_preparation_ready": gate[0].get("prime_minus_one_cuda_contract_preparation_ready"),
        "bounded_cpu_native_scored_experiment_ready": cpu_native_ready,
        "bounded_unsolved_page_micro_pilot_ready": unsolved_ready,
        "stage4p_compatibility": "compatible",
        "stage4i_compatibility": "compatible",
        "recommended_next_prompt_type": selected.get("recommended_prompt_type"),
        "recommended_next_stage_title": selected.get("recommended_stage_title"),
        "recommended_next_stage_reason": selected.get("rationale"),
        "deep_research_recommended_next": selected.get("recommended_prompt_type") == "Deep Research",
        **COMMON_TRUE_FLAGS,
        **COMMON_FALSE_FLAGS,
    }
    write_summary(summary_out, summary)
    write_json_report(out_dir, REPORT_FILES["summary"], summary)
    (out_dir / REPORT_FILES["warnings"]).write_text(json.dumps({"warnings": []}, sort_keys=True) + "\n", encoding="utf-8")
    return summary
