"""Constants for Stage 5AC prime-minus-one CUDA synthetic reporting."""

from __future__ import annotations

from pathlib import Path
from typing import Any

STAGE_ID = "stage-5ac"
SOURCE_STAGE_ID = "stage-5aa"
DOC_QUALITY_SOURCE_STAGE_ID = "stage-5ab"
SOURCE_NATIVE_PARITY_STAGE_ID = "stage-5x"
SOURCE_CONTRACT_STAGE_ID = "stage-5z"
SOURCE_MAPPING_STAGE_ID = "stage-5w"
ABI_ID = "candidate_batch_abi_v0"
CUDA_CONTRACT_ID = "prime_minus_one_stream_cuda_contract_v0"
KERNEL_ID = "prime_minus_one_stream_cuda_kernel_v0"
HASH_ALGORITHM = "sha256_canonical_json_v1"

SYNTHETIC_VECTOR_ID = "stage5z-validation-synthetic-prime-control-v0"
SYNTHETIC_MAPPING_ID = "stage5w-mapping-synthetic-prime-control-v0"
BOUNDED_P56_VECTOR_ID = "stage5z-validation-p56-bounded-v0"
BOUNDED_P56_MAPPING_ID = "stage5w-mapping-p56-stage4o-bounded-v0"
BOUNDED_P56_FIXTURE_ID = "p56-an-end-prime-minus-one"
BOUNDED_P56_CANDIDATE_ID = "stage4o-prime-minus-one-an-v0"
EXPECTED_SYNTHETIC_HASH = "06a5c37f7e5eda8eec00cfab5b09faba6ec157488ca15f61a9189d4bf06005ab"
EXPECTED_BOUNDED_P56_HASH = "4a3059f12c0f8450bd4ef7e31bf879fbc104202e5fb0e53b7ba514241f07cd87"

OUTPUT_DIR = Path("experiments/results/prime-minus-one-cuda-synthetic-reporting/stage5ac")
PARITY_REPORT_PATH = Path("data/cuda/stage5ac-prime-minus-one-cuda-synthetic-parity-report.yaml")
RESULT_STORE_INTEGRATION_PATH = Path("data/cuda/stage5ac-prime-minus-one-cuda-synthetic-result-store-integration.yaml")
SCORE_SUMMARY_INTEGRATION_PATH = Path("data/cuda/stage5ac-prime-minus-one-cuda-synthetic-score-summary-integration.yaml")
METHOD_STATUS_IMPACT_PATH = Path("data/cuda/stage5ac-prime-minus-one-cuda-synthetic-method-status-impact.yaml")
GENERATED_BODY_POLICY_PATH = Path("data/cuda/stage5ac-prime-minus-one-cuda-synthetic-generated-body-policy.yaml")
BOUNDED_P56_PREFLIGHT_PATH = Path("data/cuda/stage5ac-bounded-p56-cuda-parity-preflight.yaml")
FULL_P56_BLOCKER_PATH = Path("data/cuda/stage5ac-prime-minus-one-cuda-synthetic-full-p56-blocker.yaml")
SCORED_EXPERIMENT_DEFERRAL_PATH = Path("data/cuda/stage5ac-prime-minus-one-cuda-synthetic-scored-experiment-deferral.yaml")
DOC_STALENESS_VALIDATION_PATH = Path("data/cuda/stage5ac-prime-minus-one-cuda-synthetic-doc-staleness-validation.yaml")
NEXT_STAGE_DECISION_PATH = Path("data/cuda/stage5ac-prime-minus-one-cuda-synthetic-next-stage-decision.yaml")
SUMMARY_PATH = Path("data/cuda/stage5ac-prime-minus-one-cuda-synthetic-reporting-summary.yaml")

STAGE5AA_SUMMARY_PATH = Path("data/cuda/stage5aa-prime-minus-one-cuda-synthetic-summary.yaml")
STAGE5AA_PARITY_PATH = Path("data/cuda/stage5aa-prime-minus-one-cuda-synthetic-parity.yaml")
STAGE5AA_P56_BLOCKER_PATH = Path("data/cuda/stage5aa-prime-minus-one-cuda-synthetic-p56-blocker.yaml")
STAGE5AA_DEFERRAL_PATH = Path("data/cuda/stage5aa-prime-minus-one-cuda-synthetic-scored-experiment-deferral.yaml")
STAGE5AB_SUMMARY_PATH = Path("data/project-state/stage5ab-doc-staleness-summary.yaml")
STAGE5AB_SOURCE_OF_TRUTH_PATH = Path("data/project-state/stage5ab-doc-staleness-source-of-truth.yaml")
OPERATIONAL_FILE_MAP_PATH = Path("data/project-state/operational-file-map.yaml")
STAGE5Z_VALIDATION_PATH = Path("data/cuda/stage5z-prime-minus-one-cuda-validation-vectors.yaml")
STAGE5X_SUMMARY_PATH = Path("data/cuda/stage5x-prime-minus-one-native-parity-summary.yaml")
STAGE5W_MAPPING_PATH = Path("data/cuda/stage5w-prime-minus-one-candidate-batch-mapping.yaml")
STAGE4P_SUMMARY_PATH = Path("data/research/stage4p-result-store-score-summary-unification-summary.yaml")

REPORT_FILES = {
    "parity": "synthetic_parity_report.json",
    "result_store": "result_store_integration_report.json",
    "score_summary": "score_summary_integration_report.json",
    "method_status": "method_status_impact_report.json",
    "generated_body_policy": "generated_body_policy_report.json",
    "bounded_p56": "bounded_p56_preflight_report.json",
    "full_p56": "full_p56_blocker_report.json",
    "scored_deferral": "scored_experiment_deferral_report.json",
    "doc_staleness": "doc_staleness_validation_report.json",
    "next_stage": "next_stage_decision.json",
    "summary": "summary.json",
    "warnings": "warnings.jsonl",
}

EXPECTED_COUNTS = {
    "synthetic_parity_report_records": 1,
    "result_store_integration_records": 1,
    "score_summary_integration_records": 1,
    "method_status_impact_records": 3,
    "generated_body_policy_records": 2,
    "bounded_p56_preflight_records": 1,
    "full_p56_blocker_records": 1,
    "scored_experiment_deferral_records": 6,
    "doc_staleness_validation_records": 1,
    "next_stage_decision_records": 8,
}

COMMON_FALSE_FLAGS: dict[str, Any] = {
    "cuda_execution_performed": False,
    "cuda_source_modified": False,
    "new_cuda_kernel_added": False,
    "new_cuda_kernels_added": 0,
    "device_kernel_arithmetic_modified": False,
    "native_execution_performed": False,
    "native_cpu_execution_performed": False,
    "python_reference_execution_performed": False,
    "gpu_benchmark_performed": False,
    "benchmark_execution_allowed": False,
    "performance_claim": False,
    "speedup_claim": False,
    "scored_experiment_executed": False,
    "scored_experiment_execution_allowed": False,
    "unsolved_page_cuda_used": False,
    "unsolved_page_cuda_allowed": False,
    "real_liber_primus_cuda_data_used": False,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "generated_body_publication_allowed": False,
    "generated_outputs_committed": False,
    "raw_data_processed": False,
    "codex_output_committed": False,
    "method_status_upgrade_allowed": False,
    "method_status_upgraded": False,
    "solve_claim": False,
    "ci_gpu_required": False,
    "local_16gb_profile_required": False,
    "cxx_launches_python_workers": False,
}

COMMON_TRUE_FLAGS: dict[str, Any] = {
    "metadata_only": True,
    "reporting_only": True,
    "compact_summary_only": True,
    "no_solve_claim": True,
    "no_gpu_ci_safe": True,
}

COMMON_RECORD_FLAGS: dict[str, Any] = {
    "stage_id": STAGE_ID,
    "source_stage_id": SOURCE_STAGE_ID,
    "doc_quality_source_stage_id": DOC_QUALITY_SOURCE_STAGE_ID,
    "candidate_batch_abi_id": ABI_ID,
    "cuda_contract_id": CUDA_CONTRACT_ID,
    "kernel_id": KERNEL_ID,
    **COMMON_FALSE_FLAGS,
    **COMMON_TRUE_FLAGS,
}

NEXT_STAGE_TITLE = "Stage 5AD - bounded p56 CUDA parity run"
NEXT_STAGE_REASON = (
    "Stage 5AA synthetic prime-minus-one CUDA parity passed and Stage 5AB "
    "doc-staleness checks are clean, so the next bounded engineering step can "
    "run exactly the Stage 5Z bounded p56 vector. Full p56, unsolved pages, "
    "benchmarks, scored experiments, and generated-body publication remain blocked."
)


def base_record(record_type: str, schema: str, **extra: Any) -> dict[str, Any]:
    """Create a Stage 5AC record with shared reporting-only guardrails."""

    return {
        **COMMON_RECORD_FLAGS,
        "record_type": record_type,
        "schema": schema,
        **extra,
    }


__all__ = [
    "BOUNDED_P56_PREFLIGHT_PATH",
    "DOC_STALENESS_VALIDATION_PATH",
    "FULL_P56_BLOCKER_PATH",
    "GENERATED_BODY_POLICY_PATH",
    "METHOD_STATUS_IMPACT_PATH",
    "NEXT_STAGE_DECISION_PATH",
    "OUTPUT_DIR",
    "PARITY_REPORT_PATH",
    "RESULT_STORE_INTEGRATION_PATH",
    "SCORE_SUMMARY_INTEGRATION_PATH",
    "SCORED_EXPERIMENT_DEFERRAL_PATH",
    "SUMMARY_PATH",
    "base_record",
]
