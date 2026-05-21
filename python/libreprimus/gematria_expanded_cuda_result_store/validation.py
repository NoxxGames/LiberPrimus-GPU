"""Validate Stage 5S expanded CUDA result-store integration records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_expanded_cuda_result_store.export import read_mapping, read_record_set, read_report
from libreprimus.gematria_expanded_cuda_result_store.models import (
    BAD_TRUE_FLAGS,
    BOUNDARY_REVIEW_PATH,
    GENERATED_BODY_POLICY_PATH,
    METHOD_STATUS_IMPACT_PATH,
    NEXT_STEP_DECISION_PATH,
    OUTPUT_DIR,
    PARITY_REPORT_PATH,
    RESULT_STORE_INTEGRATION_PATH,
    SCORE_SUMMARY_INTEGRATION_PATH,
    SUMMARY_PATH,
    SUMMARY_JSON,
)


def validate_stage5s_results(
    *,
    parity_report_path: Path = PARITY_REPORT_PATH,
    result_store_integration_path: Path = RESULT_STORE_INTEGRATION_PATH,
    score_summary_integration_path: Path = SCORE_SUMMARY_INTEGRATION_PATH,
    method_status_impact_path: Path = METHOD_STATUS_IMPACT_PATH,
    generated_body_policy_path: Path = GENERATED_BODY_POLICY_PATH,
    boundary_review_path: Path = BOUNDARY_REVIEW_PATH,
    next_step_decision_path: Path = NEXT_STEP_DECISION_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, int | bool], list[str]]:
    parity = read_record_set(parity_report_path)
    result_store = read_record_set(result_store_integration_path)
    score = read_record_set(score_summary_integration_path)
    method = read_record_set(method_status_impact_path)
    policy = read_record_set(generated_body_policy_path)
    boundary = read_record_set(boundary_review_path)
    decisions = read_record_set(next_step_decision_path)
    summary = read_mapping(summary_path)
    errors: list[str] = []
    expected_counts = {
        "parity_report_records": 3,
        "result_store_integration_records": 3,
        "score_summary_integration_records": 3,
        "method_status_impact_records": 7,
        "generated_body_policy_records": 4,
        "boundary_review_records": 1,
        "controlled_next_step_decision_records": 6,
    }
    actual = {
        "parity_report_records": len(parity),
        "result_store_integration_records": len(result_store),
        "score_summary_integration_records": len(score),
        "method_status_impact_records": len(method),
        "generated_body_policy_records": len(policy),
        "boundary_review_records": len(boundary),
        "controlled_next_step_decision_records": len(decisions),
    }
    for key, expected in expected_counts.items():
        if actual[key] != expected:
            errors.append(f"{key}={actual[key]} expected {expected}")
    all_records: list[dict[str, Any]] = [*parity, *result_store, *score, *method, *policy, *boundary, *decisions, summary]
    for record in all_records:
        for flag in BAD_TRUE_FLAGS:
            if record.get(flag) is True:
                errors.append(f"{record.get('record_type', 'summary')} has forbidden true flag {flag}")
        if record.get("no_solve_claim") is not True:
            errors.append(f"{record.get('record_type', 'summary')} missing no_solve_claim=true")
    if any(record.get("parity_status") != "passed" for record in parity):
        errors.append("all parity report records must be passed")
    if any(record.get("stage4p_compatibility") is not True for record in result_store):
        errors.append("all result-store records must cite Stage 4P compatibility")
    if any(record.get("scorer_contract") != "stage4i" for record in score):
        errors.append("all score-summary records must cite Stage 4I")
    if any(record.get("upgraded_to_solved") for record in method):
        errors.append("method-status records must not upgrade to solved")
    if not any(record.get("selected") and record.get("deep_research_recommended") for record in decisions):
        errors.append("one Deep Research next-step decision must be selected")
    if summary.get("selected_next_prompt") is None:
        errors.append("summary missing selected_next_prompt")
    try:
        read_report(results_dir, SUMMARY_JSON)
    except FileNotFoundError:
        errors.append("missing ignored Stage 5S summary report")
    counts: dict[str, int | bool] = {
        **actual,
        "stage4p_compatibility": all(record.get("stage4p_compatibility") is True for record in result_store),
        "stage4i_compatibility": all(record.get("scorer_contract") == "stage4i" for record in score),
        "deep_research_recommended": summary.get("deep_research_recommended") is True,
    }
    return counts, errors
