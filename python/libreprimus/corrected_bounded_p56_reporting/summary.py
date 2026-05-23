"""Build the committed Stage 5AE corrected reporting summary."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_records, write_json_report, write_summary, write_warnings
from .models import (
    ARCHIVE_SOURCE_LOCK_DEFERRAL_PATH,
    CORRECTED_FORMULA_HASH,
    DOC_STALENESS_VALIDATION_PATH,
    EXPECTED_COUNTS,
    FORMULA_PARITY_REPORT_PATH,
    FULL_P56_BLOCKER_PATH,
    GENERATED_BODY_POLICY_PATH,
    HASH_MATERIAL_POLICY_PATH,
    HISTORICAL_COMPUTED_CUDA_HASH,
    HISTORICAL_EXPECTED_HASH,
    METHOD_STATUS_IMPACT_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    REFERENCE_CONTRACT_REPAIR_PATH,
    REPORT_FILES,
    RESULT_STORE_INTEGRATION_PATH,
    SCORE_SUMMARY_INTEGRATION_PATH,
    SCORED_EXPERIMENT_DEFERRAL_PATH,
    SELECTED_NEXT_OPTION_ID,
    SUMMARY_PATH,
    SYNTHETIC_CONTROL_HASH,
)


def build_summary(
    *,
    formula_parity_report: Path = FORMULA_PARITY_REPORT_PATH,
    reference_contract_repair: Path = REFERENCE_CONTRACT_REPAIR_PATH,
    hash_material_policy: Path = HASH_MATERIAL_POLICY_PATH,
    result_store_integration: Path = RESULT_STORE_INTEGRATION_PATH,
    score_summary_integration: Path = SCORE_SUMMARY_INTEGRATION_PATH,
    method_status_impact: Path = METHOD_STATUS_IMPACT_PATH,
    generated_body_policy: Path = GENERATED_BODY_POLICY_PATH,
    full_p56_blocker: Path = FULL_P56_BLOCKER_PATH,
    scored_experiment_deferral: Path = SCORED_EXPERIMENT_DEFERRAL_PATH,
    archive_source_lock_deferral: Path = ARCHIVE_SOURCE_LOCK_DEFERRAL_PATH,
    doc_staleness_validation: Path = DOC_STALENESS_VALIDATION_PATH,
    next_stage_decision: Path = NEXT_STAGE_DECISION_PATH,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    groups = {
        "corrected_formula_parity_report_records": read_records(formula_parity_report),
        "reference_contract_repair_records": read_records(reference_contract_repair),
        "hash_material_policy_records": read_records(hash_material_policy),
        "result_store_integration_records": read_records(result_store_integration),
        "score_summary_integration_records": read_records(score_summary_integration),
        "method_status_impact_records": read_records(method_status_impact),
        "generated_body_policy_records": read_records(generated_body_policy),
        "full_p56_blocker_records": read_records(full_p56_blocker),
        "scored_experiment_deferral_records": read_records(scored_experiment_deferral),
        "archive_source_lock_deferral_records": read_records(archive_source_lock_deferral),
        "doc_staleness_validation_records": read_records(doc_staleness_validation),
        "next_stage_decision_records": read_records(next_stage_decision),
    }
    formula = groups["corrected_formula_parity_report_records"][0]
    decision = next(record for record in groups["next_stage_decision_records"] if record.get("selected") is True)
    summary: dict[str, Any] = {
        "record_type": "stage5ae_corrected_bounded_p56_reporting_summary",
        "schema": "schemas/cuda/stage5ae-corrected-bounded-p56-reporting-summary-v0.schema.json",
        "stage_id": "stage-5ae",
        "status": "complete",
        "source_stage_id": "stage-5ad-fix",
        "historical_failed_stage_id": "stage-5ad",
        "source_formula_stage_id": "stage-5x",
        "source_reference_stage_id": "stage-5l",
        "source_contract_stage_id": "stage-5w",
        "candidate_batch_abi_id": "candidate_batch_abi_v0",
        "cuda_contract_id": "prime_minus_one_stream_cuda_contract_v0",
        "kernel_id": "prime_minus_one_stream_cuda_kernel_v0",
        "bounded_p56_vector_id": "stage5z-validation-p56-bounded-v0",
        "mapping_id": "stage5w-mapping-p56-stage4o-bounded-v0",
        "fixture_id": "p56-an-end-prime-minus-one",
        "candidate_id": "stage4o-prime-minus-one-an-v0",
        "token_mapping_id": "stage5l-token-mapping-04",
        "historical_stage5ad_status": "failed_hash_mismatch",
        "historical_stage5ad_failure_preserved": True,
        "historical_stage5ad_reclassified_as_passed": False,
        "historical_stage5ad_expected_hash": HISTORICAL_EXPECTED_HASH,
        "historical_stage5ad_computed_cuda_hash": HISTORICAL_COMPUTED_CUDA_HASH,
        "corrected_formula_expected_hash": formula["corrected_formula_expected_hash"],
        "corrected_formula_computed_hash": formula["corrected_formula_computed_hash"],
        "corrected_formula_parity_status": formula["corrected_formula_parity_status"],
        "corrected_formula_reference_source": formula["corrected_formula_reference_source"],
        "stage5x_formula_hash": CORRECTED_FORMULA_HASH,
        "stage5aa_synthetic_reference_hash": SYNTHETIC_CONTROL_HASH,
        "reference_contract_repair_complete": True,
        "hash_material_policy_repair_complete": True,
        "cuda_kernel_repair_required": False,
        "archive_source_lock_ready_next": decision["archive_source_lock_ready_next"],
        "recommended_next_option_id": decision["option_id"],
        "recommended_next_prompt_type": decision["recommended_prompt_type"],
        "recommended_next_stage_title": decision["recommended_stage_title"],
        "recommended_next_stage_reason": decision["rationale"],
        "deep_research_recommended_next": decision["deep_research_recommended_next"],
        "cuda_execution_performed": False,
        "bounded_p56_cuda_executed": False,
        "full_p56_cuda_executed": False,
        "full_p56_cuda_allowed": False,
        "unsolved_page_cuda_used": False,
        "unsolved_page_cuda_allowed": False,
        "real_liber_primus_cuda_data_used": False,
        "raw_data_processed": False,
        "archive_raw_data_processed": False,
        "native_execution_performed": False,
        "python_reference_execution_performed": False,
        "gpu_benchmark_performed": False,
        "benchmark_execution_allowed": False,
        "performance_claim": False,
        "speedup_claim": False,
        "scored_experiment_executed": False,
        "scored_experiment_execution_allowed": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "website_expansion_performed": False,
        "generated_body_publication_allowed": False,
        "generated_outputs_committed": False,
        "codex_output_committed": False,
        "method_status_upgrade_allowed": False,
        "method_status_upgraded": False,
        "solve_claim": False,
        "no_solve_claim": True,
        "cuda_source_modified": False,
        "new_cuda_kernel_added": False,
        "new_cuda_kernels_added": 0,
        "device_kernel_arithmetic_modified": False,
        "ci_gpu_required": False,
        "local_16gb_profile_required": False,
        "cxx_launches_python_workers": False,
        "no_gpu_ci_safe": True,
    }
    for key, records in groups.items():
        summary[key] = len(records)
    for key, expected in EXPECTED_COUNTS.items():
        summary.setdefault(key, expected)
    if decision["option_id"] != SELECTED_NEXT_OPTION_ID:
        raise ValueError("Stage 5AE selected an unexpected next stage.")
    write_summary(summary_out, summary)
    write_json_report(out_dir, REPORT_FILES["summary"], summary)
    write_warnings(out_dir, ["stage5ad_failure_preserved_corrected_formula_parity_recorded"])
    return summary
