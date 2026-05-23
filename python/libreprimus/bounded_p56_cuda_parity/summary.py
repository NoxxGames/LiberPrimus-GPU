"""Build the committed Stage 5AD summary."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_records, write_json_report, write_summary, write_warnings
from .models import (
    CUDA_PARITY_PATH,
    CUDA_RUN_PATH,
    DEVICE_SUBSET_AUDIT_PATH,
    DOC_STALENESS_VALIDATION_PATH,
    EXPECTED_COUNTS,
    EXPECTED_OUTPUT_TOKEN_HASH,
    FULL_P56_BLOCKER_PATH,
    HASH_ALGORITHM,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    REPORT_FILES,
    RESULT_STORE_PREFLIGHT_PATH,
    SCORE_SUMMARY_PREFLIGHT_PATH,
    SCORED_EXPERIMENT_DEFERRAL_PATH,
    SOURCE_SYNTHETIC_HASH,
    SUMMARY_PATH,
)


def build_summary(
    *,
    cuda_run: Path = CUDA_RUN_PATH,
    cuda_parity: Path = CUDA_PARITY_PATH,
    result_store_preflight: Path = RESULT_STORE_PREFLIGHT_PATH,
    score_summary_preflight: Path = SCORE_SUMMARY_PREFLIGHT_PATH,
    full_p56_blocker: Path = FULL_P56_BLOCKER_PATH,
    scored_experiment_deferral: Path = SCORED_EXPERIMENT_DEFERRAL_PATH,
    doc_staleness_validation: Path = DOC_STALENESS_VALIDATION_PATH,
    device_subset_audit: Path = DEVICE_SUBSET_AUDIT_PATH,
    next_stage_decision: Path = NEXT_STAGE_DECISION_PATH,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    run_records = read_records(cuda_run)
    parity_records = read_records(cuda_parity)
    result_store_records = read_records(result_store_preflight)
    score_records = read_records(score_summary_preflight)
    full_records = read_records(full_p56_blocker)
    deferral_records = read_records(scored_experiment_deferral)
    doc_records = read_records(doc_staleness_validation)
    audit_records = read_records(device_subset_audit)
    decision_records = read_records(next_stage_decision)
    run = run_records[0]
    parity = parity_records[0]
    selected = next(record for record in decision_records if record.get("selected") is True)
    stage5ae_ready = parity.get("parity_status") == "passed"
    summary: dict[str, Any] = {
        "record_type": "stage5ad_bounded_p56_cuda_parity_summary",
        "stage_id": "stage-5ad",
        "status": "complete",
        "source_stage_id": "stage-5ac",
        "source_synthetic_stage_id": "stage-5aa",
        "source_native_stage_id": "stage-5x",
        "doc_quality_source_stage_id": "stage-5ab",
        "candidate_batch_abi_id": "candidate_batch_abi_v0",
        "cuda_contract_id": "prime_minus_one_stream_cuda_contract_v0",
        "kernel_id": "prime_minus_one_stream_cuda_kernel_v0",
        "kernel_entrypoint": "prime_minus_one_stream_kernel_v0",
        "bounded_p56_vector_id": run["validation_vector_id"],
        "mapping_id": run["mapping_id"],
        "fixture_id": run["fixture_id"],
        "candidate_id": run["candidate_id"],
        "expected_output_token_hash": EXPECTED_OUTPUT_TOKEN_HASH,
        "computed_cuda_output_token_hash": run.get("computed_cuda_output_token_hash"),
        "cuda_kernel_formula_output_token_hash": run.get("cuda_kernel_formula_output_token_hash"),
        "source_stage5aa_expected_hash": SOURCE_SYNTHETIC_HASH,
        "output_hash_algorithm": HASH_ALGORITHM,
        "cuda_run_records": len(run_records),
        "cuda_parity_records": len(parity_records),
        "result_store_preflight_records": len(result_store_records),
        "score_summary_preflight_records": len(score_records),
        "full_p56_blocker_records": len(full_records),
        "scored_experiment_deferral_records": len(deferral_records),
        "doc_staleness_validation_records": len(doc_records),
        "device_subset_audit_records": len(audit_records),
        "next_stage_decision_records": len(decision_records),
        "cuda_attempted_count": run["cuda_attempted_count"],
        "cuda_pass_count": run["cuda_pass_count"],
        "cuda_fail_count": run["cuda_fail_count"],
        "cuda_skip_count": run["cuda_skip_count"],
        "stage5x_expected_hash_match_count": 1 if parity.get("stage5x_expected_hash_match") else 0,
        "stage5ad_parity_status": parity["parity_status"],
        "stage5ae_ready": stage5ae_ready,
        "full_p56_status": full_records[0]["full_p56_status"],
        "scored_experiments_status": "deferred_manifest_gate_required",
        "website_expansion_status": "deferred_future_unnumbered_project",
        "visual_clue_deep_research_status": "deferred_future_review",
        "recommended_next_prompt_type": selected["recommended_prompt_type"],
        "recommended_next_stage_title": selected["recommended_stage_title"],
        "recommended_next_stage_reason": selected["rationale"],
        "deep_research_recommended_next": False,
        "bounded_p56_cuda_executed": run["bounded_p56_cuda_executed"],
        "cuda_execution_performed": run["cuda_execution_performed"],
        "cuda_source_modified": audit_records[0]["cuda_source_modified"],
        "device_kernel_arithmetic_modified": audit_records[0]["device_kernel_arithmetic_modified"],
        "new_cuda_kernel_added": False,
        "new_cuda_kernels_added": 0,
        "full_p56_cuda_executed": False,
        "unsolved_page_cuda_used": False,
        "unsolved_page_cuda_allowed": False,
        "real_liber_primus_cuda_data_used": False,
        "raw_data_processed": False,
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
        "generated_body_publication_allowed": False,
        "generated_outputs_committed": False,
        "codex_output_committed": False,
        "method_status_upgrade_allowed": False,
        "method_status_upgraded": False,
        "solve_claim": False,
        "no_solve_claim": True,
        "no_gpu_ci_safe": True,
        "ci_gpu_required": False,
        "local_16gb_profile_required": False,
        "cxx_launches_python_workers": False,
    }
    for key, expected in EXPECTED_COUNTS.items():
        summary.setdefault(key, expected)
    write_summary(summary_out, summary)
    write_json_report(out_dir, REPORT_FILES["summary"], summary)
    write_warnings(out_dir, ["bounded_p56_cuda_hash_mismatch"] if summary["stage5ad_parity_status"] == "failed_hash_mismatch" else [])
    return summary
