"""Build the committed Stage 5AC summary."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_cuda_synthetic_reporting.export import read_records, write_json_report, write_summary, write_warnings
from libreprimus.prime_minus_one_cuda_synthetic_reporting.models import (
    BOUNDED_P56_PREFLIGHT_PATH,
    COMMON_FALSE_FLAGS,
    COMMON_TRUE_FLAGS,
    DOC_QUALITY_SOURCE_STAGE_ID,
    DOC_STALENESS_VALIDATION_PATH,
    EXPECTED_COUNTS,
    FULL_P56_BLOCKER_PATH,
    GENERATED_BODY_POLICY_PATH,
    METHOD_STATUS_IMPACT_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    PARITY_REPORT_PATH,
    REPORT_FILES,
    RESULT_STORE_INTEGRATION_PATH,
    SCORE_SUMMARY_INTEGRATION_PATH,
    SCORED_EXPERIMENT_DEFERRAL_PATH,
    SOURCE_STAGE_ID,
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
    bounded_p56_preflight: Path = BOUNDED_P56_PREFLIGHT_PATH,
    full_p56_blocker: Path = FULL_P56_BLOCKER_PATH,
    scored_experiment_deferral: Path = SCORED_EXPERIMENT_DEFERRAL_PATH,
    doc_staleness_validation: Path = DOC_STALENESS_VALIDATION_PATH,
    next_stage_decision: Path = NEXT_STAGE_DECISION_PATH,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    groups = {
        "synthetic_parity_report_records": read_records(parity_report),
        "result_store_integration_records": read_records(result_store_integration),
        "score_summary_integration_records": read_records(score_summary_integration),
        "method_status_impact_records": read_records(method_status_impact),
        "generated_body_policy_records": read_records(generated_body_policy),
        "bounded_p56_preflight_records": read_records(bounded_p56_preflight),
        "full_p56_blocker_records": read_records(full_p56_blocker),
        "scored_experiment_deferral_records": read_records(scored_experiment_deferral),
        "doc_staleness_validation_records": read_records(doc_staleness_validation),
        "next_stage_decision_records": read_records(next_stage_decision),
    }
    parity = groups["synthetic_parity_report_records"][0]
    preflight = groups["bounded_p56_preflight_records"][0]
    full_p56 = groups["full_p56_blocker_records"][0]
    selected = next(record for record in groups["next_stage_decision_records"] if record.get("selected") is True)
    doc = groups["doc_staleness_validation_records"][0]
    summary = {
        "record_type": "stage5ac_prime_minus_one_cuda_synthetic_reporting_summary",
        "schema": "schemas/cuda/stage5ac-prime-minus-one-cuda-synthetic-reporting-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "status": "complete",
        "source_stage_id": SOURCE_STAGE_ID,
        "doc_quality_source_stage_id": DOC_QUALITY_SOURCE_STAGE_ID,
        "candidate_batch_abi_id": "candidate_batch_abi_v0",
        "cuda_contract_id": "prime_minus_one_stream_cuda_contract_v0",
        "kernel_id": "prime_minus_one_stream_cuda_kernel_v0",
        "source_stage5aa_cuda_pass_count": parity.get("source_stage5aa_cuda_pass_count"),
        "source_stage5aa_cuda_fail_count": parity.get("source_stage5aa_cuda_fail_count"),
        "source_stage5aa_cuda_skip_count": parity.get("source_stage5aa_cuda_skip_count"),
        "source_stage5aa_expected_hash": parity.get("expected_output_token_hash"),
        "source_stage5aa_computed_hash": parity.get("computed_output_token_hash"),
        "stage5aa_hash_match": parity.get("stage5aa_hash_match") is True,
        "stage5ab_doc_staleness_strict_pass": doc.get("doc_staleness_strict_check_passed") is True,
        "bounded_p56_preflight_status": preflight.get("preflight_status"),
        "bounded_p56_cuda_ready_next_stage": preflight.get("bounded_p56_cuda_execution_ready_next_stage"),
        "full_p56_status": full_p56.get("full_p56_status"),
        "scored_experiments_status": "deferred_manifest_gate_required",
        "website_expansion_status": "deferred_future_unnumbered_project",
        "recommended_next_prompt_type": selected.get("recommended_prompt_type"),
        "recommended_next_stage_title": selected.get("recommended_stage_title"),
        "recommended_next_stage_reason": selected.get("rationale"),
        "deep_research_recommended_next": selected.get("recommended_prompt_type") == "Deep Research",
        **COMMON_FALSE_FLAGS,
        **COMMON_TRUE_FLAGS,
    }
    summary.update({key: len(records) for key, records in groups.items()})
    summary.update({key: value for key, value in EXPECTED_COUNTS.items() if key not in summary})
    write_summary(summary_out, summary)
    write_json_report(out_dir, REPORT_FILES["summary"], summary)
    write_warnings(out_dir, [])
    return summary
