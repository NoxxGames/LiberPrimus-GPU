"""Constants for Stage 5AA prime-minus-one CUDA synthetic parity records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

STAGE_ID = "stage-5aa"
SOURCE_STAGE_ID = "stage-5z"
SOURCE_NATIVE_PARITY_STAGE_ID = "stage-5x"
SOURCE_CONTRACT_STAGE_ID = "stage-5w"
ABI_ID = "candidate_batch_abi_v0"
CUDA_CONTRACT_ID = "prime_minus_one_stream_cuda_contract_v0"
KERNEL_ID = "prime_minus_one_stream_cuda_kernel_v0"
KERNEL_ENTRYPOINT = "prime_minus_one_stream_kernel_v0"
VALIDATION_VECTOR_ID = "stage5z-validation-synthetic-prime-control-v0"
SYNTHETIC_MAPPING_ID = "stage5w-mapping-synthetic-prime-control-v0"
SYNTHETIC_FIXTURE_ID = "stage5w-synthetic-prime-minus-one-control"
HASH_ALGORITHM = "sha256_canonical_json_v1"
EXPECTED_SYNTHETIC_HASH = "06a5c37f7e5eda8eec00cfab5b09faba6ec157488ca15f61a9189d4bf06005ab"

SYNTHETIC_INPUT_TOKENS = [
    {"position": 0, "token_kind": "rune", "transformable": True, "index29": 0},
    {"position": 1, "token_kind": "rune", "transformable": True, "index29": 2},
    {"position": 2, "token_kind": "word_separator", "transformable": False, "index29": -1},
    {"position": 3, "token_kind": "rune", "transformable": True, "index29": 2},
]
SYNTHETIC_OUTPUT_TOKENS = [
    {"position": 0, "token_kind": "rune", "transformable": True, "index29": 28},
    {"position": 1, "token_kind": "rune", "transformable": True, "index29": 0},
    {"position": 2, "token_kind": "word_separator", "transformable": False, "index29": -1},
    {"position": 3, "token_kind": "rune", "transformable": True, "index29": 27},
]
SYNTHETIC_STREAM_VALUES_USED = [1, 2, 4]

OUTPUT_DIR = Path("experiments/results/prime-minus-one-cuda-synthetic/stage5aa")
KERNEL_IMPLEMENTATION_PATH = Path("data/cuda/stage5aa-prime-minus-one-cuda-synthetic-kernel-implementation.yaml")
CUDA_RUN_PATH = Path("data/cuda/stage5aa-prime-minus-one-cuda-synthetic-run.yaml")
PARITY_PATH = Path("data/cuda/stage5aa-prime-minus-one-cuda-synthetic-parity.yaml")
DEVICE_SUBSET_AUDIT_PATH = Path("data/cuda/stage5aa-prime-minus-one-cuda-device-subset-audit.yaml")
RESULT_STORE_PREFLIGHT_PATH = Path("data/cuda/stage5aa-prime-minus-one-cuda-synthetic-result-store-preflight.yaml")
P56_BLOCKER_PATH = Path("data/cuda/stage5aa-prime-minus-one-cuda-synthetic-p56-blocker.yaml")
SCORED_EXPERIMENT_DEFERRAL_PATH = Path("data/cuda/stage5aa-prime-minus-one-cuda-synthetic-scored-experiment-deferral.yaml")
NEXT_STAGE_DECISION_PATH = Path("data/cuda/stage5aa-prime-minus-one-cuda-synthetic-next-stage-decision.yaml")
SUMMARY_PATH = Path("data/cuda/stage5aa-prime-minus-one-cuda-synthetic-summary.yaml")

STAGE5Z_VALIDATION_PATH = Path("data/cuda/stage5z-prime-minus-one-cuda-validation-vectors.yaml")
STAGE5Z_SUMMARY_PATH = Path("data/cuda/stage5z-prime-minus-one-cuda-contract-summary.yaml")
STAGE5X_PARITY_PATH = Path("data/cuda/stage5x-prime-minus-one-native-parity.yaml")

CUDA_HEADER = Path("cuda/include/libreprimus/prime_minus_one_stream_kernel.cuh")
CUDA_SOURCE = Path("cuda/kernels/prime_minus_one_stream_kernel.cu")
CUDA_TEST = Path("cuda/tests/prime_minus_one_stream_kernel_test.cpp")

REPORT_FILES = {
    "kernel_build": "kernel_build_report.json",
    "cuda_run": "cuda_run_report.json",
    "parity": "parity_report.json",
    "device_audit": "device_subset_audit.json",
    "result_store": "result_store_preflight_report.json",
    "p56_blocker": "p56_blocker_report.json",
    "scored_deferral": "scored_experiment_deferral_report.json",
    "next_stage": "next_stage_decision.json",
    "summary": "summary.json",
    "warnings": "warnings.jsonl",
}

EXPECTED_COUNTS = {
    "kernel_implementation_records": 1,
    "cuda_run_records": 1,
    "parity_records": 1,
    "device_subset_audit_records": 1,
    "result_store_preflight_records": 2,
    "p56_blocker_records": 2,
    "scored_experiment_deferral_records": 6,
    "next_stage_decision_records": 4,
}

FORBIDDEN_FALSE_FLAGS = {
    "p56_cuda_execution_performed": False,
    "full_p56_cuda_execution_performed": False,
    "unsolved_page_cuda_used": False,
    "unsolved_page_cuda_allowed": False,
    "real_liber_primus_cuda_data_used": False,
    "gpu_benchmark_performed": False,
    "benchmark_execution_allowed": False,
    "performance_claim": False,
    "speedup_claim": False,
    "scored_experiment_executed": False,
    "scored_experiment_execution_allowed": False,
    "website_expansion_performed": False,
    "website_expansion_allowed": False,
    "generated_body_publication_allowed": False,
    "generated_outputs_committed": False,
    "raw_data_processed": False,
    "codex_output_committed": False,
    "method_status_upgrade_allowed": False,
    "method_status_upgraded": False,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "solve_claim": False,
    "ci_gpu_required": False,
    "local_16gb_profile_required": False,
    "cxx_launches_python_workers": False,
}

COMMON_RECORD_FLAGS: dict[str, Any] = {
    "stage_id": STAGE_ID,
    "source_stage_id": SOURCE_STAGE_ID,
    "source_native_parity_stage_id": SOURCE_NATIVE_PARITY_STAGE_ID,
    "source_contract_stage_id": SOURCE_CONTRACT_STAGE_ID,
    "candidate_batch_abi_id": ABI_ID,
    "cuda_contract_id": CUDA_CONTRACT_ID,
    "kernel_id": KERNEL_ID,
    "synthetic_only": True,
    "native_cpu_execution_performed": False,
    "native_execution_performed": False,
    "python_reference_execution_performed": False,
    "cuda_source_modified": True,
    "new_cuda_kernel_added": True,
    "new_cuda_kernels_added": 1,
    "device_kernel_arithmetic_modified": True,
    "no_solve_claim": True,
    "no_gpu_ci_safe": True,
    **FORBIDDEN_FALSE_FLAGS,
}

NEXT_STAGE_IF_PASSED = "Stage 5AB - prime-minus-one CUDA synthetic parity reporting and bounded-p56 CUDA parity preflight"
NEXT_STAGE_IF_SKIPPED = "Stage 5AA-followup - prime-minus-one CUDA synthetic toolchain repair and rerun"
NEXT_STAGE_IF_MISMATCH = "Stage 5AA-fix - prime-minus-one CUDA synthetic parity mismatch investigation"


def base_record(record_type: str, schema: str, **extra: Any) -> dict[str, Any]:
    """Create a Stage 5AA record with shared guardrails."""

    return {
        **COMMON_RECORD_FLAGS,
        "record_type": record_type,
        "schema": schema,
        **extra,
    }


__all__ = [
    "CUDA_RUN_PATH",
    "DEVICE_SUBSET_AUDIT_PATH",
    "EXPECTED_SYNTHETIC_HASH",
    "KERNEL_IMPLEMENTATION_PATH",
    "NEXT_STAGE_DECISION_PATH",
    "OUTPUT_DIR",
    "P56_BLOCKER_PATH",
    "PARITY_PATH",
    "RESULT_STORE_PREFLIGHT_PATH",
    "SCORED_EXPERIMENT_DEFERRAL_PATH",
    "SUMMARY_PATH",
    "base_record",
]
