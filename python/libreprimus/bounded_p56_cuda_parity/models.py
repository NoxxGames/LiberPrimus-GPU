"""Constants for Stage 5AD bounded p56 CUDA parity records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

STAGE_ID = "stage-5ad"
SOURCE_STAGE_ID = "stage-5ac"
SOURCE_SYNTHETIC_STAGE_ID = "stage-5aa"
SOURCE_NATIVE_STAGE_ID = "stage-5x"
SOURCE_CONTRACT_STAGE_ID = "stage-5z"
SOURCE_MAPPING_STAGE_ID = "stage-5w"
DOC_QUALITY_SOURCE_STAGE_ID = "stage-5ab"
ABI_ID = "candidate_batch_abi_v0"
CUDA_CONTRACT_ID = "prime_minus_one_stream_cuda_contract_v0"
KERNEL_ID = "prime_minus_one_stream_cuda_kernel_v0"
KERNEL_ENTRYPOINT = "prime_minus_one_stream_kernel_v0"
HASH_ALGORITHM = "sha256_canonical_json_v1"

VALIDATION_VECTOR_ID = "stage5z-validation-p56-bounded-v0"
MAPPING_ID = "stage5w-mapping-p56-stage4o-bounded-v0"
FIXTURE_ID = "p56-an-end-prime-minus-one"
CANDIDATE_ID = "stage4o-prime-minus-one-an-v0"
STREAM_SCHEDULE_REF = "stage5w-p56-stage4o-bounded-prime-minus-one-schedule-v0"
EXPECTED_OUTPUT_TOKEN_HASH = "4a3059f12c0f8450bd4ef7e31bf879fbc104202e5fb0e53b7ba514241f07cd87"
FORMULA_OUTPUT_TOKEN_HASH = "6034fe2431159615449db79c36869236d306768414038314d47d6d57d9ae7387"
SOURCE_SYNTHETIC_HASH = "06a5c37f7e5eda8eec00cfab5b09faba6ec157488ca15f61a9189d4bf06005ab"

TOKEN_COUNT = 2
TRANSFORMABLE_TOKEN_COUNT = 2
SEPARATOR_COUNT = 0
STREAM_START_INDEX = 0
STREAM_VALUES_USED = [1, 2]
INPUT_TOKENS = [
    {"position": 0, "token_kind": "rune", "transformable": True, "index29": 25, "raw_text": None},
    {"position": 1, "token_kind": "rune", "transformable": True, "index29": 11, "raw_text": None},
]
FORMULA_OUTPUT_TOKENS = [
    {"position": 0, "token_kind": "rune", "transformable": True, "index29": 24, "raw_text": None},
    {"position": 1, "token_kind": "rune", "transformable": True, "index29": 9, "raw_text": None},
]

OUTPUT_DIR = Path("experiments/results/prime-minus-one-bounded-p56-cuda-parity/stage5ad")
CUDA_RUN_PATH = Path("data/cuda/stage5ad-bounded-p56-cuda-run.yaml")
CUDA_PARITY_PATH = Path("data/cuda/stage5ad-bounded-p56-cuda-parity.yaml")
RESULT_STORE_PREFLIGHT_PATH = Path("data/cuda/stage5ad-bounded-p56-cuda-result-store-preflight.yaml")
SCORE_SUMMARY_PREFLIGHT_PATH = Path("data/cuda/stage5ad-bounded-p56-cuda-score-summary-preflight.yaml")
FULL_P56_BLOCKER_PATH = Path("data/cuda/stage5ad-bounded-p56-cuda-full-p56-blocker.yaml")
SCORED_EXPERIMENT_DEFERRAL_PATH = Path("data/cuda/stage5ad-bounded-p56-cuda-scored-experiment-deferral.yaml")
DOC_STALENESS_VALIDATION_PATH = Path("data/cuda/stage5ad-bounded-p56-cuda-doc-staleness-validation.yaml")
DEVICE_SUBSET_AUDIT_PATH = Path("data/cuda/stage5ad-bounded-p56-cuda-device-subset-audit.yaml")
NEXT_STAGE_DECISION_PATH = Path("data/cuda/stage5ad-bounded-p56-cuda-next-stage-decision.yaml")
SUMMARY_PATH = Path("data/cuda/stage5ad-bounded-p56-cuda-parity-summary.yaml")

STAGE5AC_SUMMARY_PATH = Path("data/cuda/stage5ac-prime-minus-one-cuda-synthetic-reporting-summary.yaml")
STAGE5AC_PREFLIGHT_PATH = Path("data/cuda/stage5ac-bounded-p56-cuda-parity-preflight.yaml")
STAGE5AA_PARITY_PATH = Path("data/cuda/stage5aa-prime-minus-one-cuda-synthetic-parity.yaml")
STAGE5X_RUN_PATH = Path("data/cuda/stage5x-prime-minus-one-native-run.yaml")
STAGE5W_MAPPING_PATH = Path("data/cuda/stage5w-prime-minus-one-candidate-batch-mapping.yaml")
STAGE5Z_VALIDATION_PATH = Path("data/cuda/stage5z-prime-minus-one-cuda-validation-vectors.yaml")
STAGE5AB_SOURCE_OF_TRUTH_PATH = Path("data/project-state/stage5ab-doc-staleness-source-of-truth.yaml")
OPERATIONAL_FILE_MAP_PATH = Path("data/project-state/operational-file-map.yaml")

REPORT_FILES = {
    "cuda_run": "cuda_run_report.json",
    "parity": "parity_report.json",
    "result_store": "result_store_preflight_report.json",
    "score_summary": "score_summary_preflight_report.json",
    "full_p56": "full_p56_blocker_report.json",
    "scored_deferral": "scored_experiment_deferral_report.json",
    "doc_staleness": "doc_staleness_validation_report.json",
    "device_audit": "device_subset_audit.json",
    "next_stage": "next_stage_decision.json",
    "summary": "summary.json",
    "warnings": "warnings.jsonl",
}

EXPECTED_COUNTS = {
    "cuda_run_records": 1,
    "cuda_parity_records": 1,
    "result_store_preflight_records": 1,
    "score_summary_preflight_records": 1,
    "full_p56_blocker_records": 1,
    "scored_experiment_deferral_records": 7,
    "doc_staleness_validation_records": 1,
    "device_subset_audit_records": 1,
    "next_stage_decision_records": 10,
}

COMMON_FALSE_FLAGS: dict[str, Any] = {
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
    "ci_gpu_required": False,
    "local_16gb_profile_required": False,
    "cxx_launches_python_workers": False,
}

COMMON_RECORD_FLAGS: dict[str, Any] = {
    "stage_id": STAGE_ID,
    "source_stage_id": SOURCE_STAGE_ID,
    "source_synthetic_stage_id": SOURCE_SYNTHETIC_STAGE_ID,
    "source_native_stage_id": SOURCE_NATIVE_STAGE_ID,
    "source_contract_stage_id": SOURCE_CONTRACT_STAGE_ID,
    "doc_quality_source_stage_id": DOC_QUALITY_SOURCE_STAGE_ID,
    "candidate_batch_abi_id": ABI_ID,
    "cuda_contract_id": CUDA_CONTRACT_ID,
    "kernel_id": KERNEL_ID,
    "kernel_entrypoint": KERNEL_ENTRYPOINT,
    "cuda_source_modified": False,
    "new_cuda_kernel_added": False,
    "new_cuda_kernels_added": 0,
    "device_kernel_arithmetic_modified": False,
    "no_solve_claim": True,
    "no_gpu_ci_safe": True,
    **COMMON_FALSE_FLAGS,
}

NEXT_STAGE_IF_PASSED = "Stage 5AE - bounded p56 CUDA parity reporting and full-p56/source-expansion gate"
NEXT_STAGE_IF_SKIPPED = "Stage 5AD-followup - bounded p56 CUDA toolchain repair and rerun"
NEXT_STAGE_IF_MISMATCH = "Stage 5AD-fix - bounded p56 CUDA parity mismatch investigation"


def base_record(record_type: str, schema: str, **extra: Any) -> dict[str, Any]:
    return {
        **COMMON_RECORD_FLAGS,
        "record_type": record_type,
        "schema": schema,
        **extra,
    }
