"""Constants for Stage 5Z prime-minus-one CUDA contract records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

STAGE_ID = "stage-5z"
SOURCE_STAGE_ID = "stage-5y"
SOURCE_PARITY_STAGE_ID = "stage-5x"
SOURCE_CONTRACT_STAGE_ID = "stage-5w"
ABI_ID = "candidate_batch_abi_v0"
SOURCE_NATIVE_CONTRACT_ID = "prime_minus_one_stream_native_contract_v0"
CUDA_CONTRACT_ID = "prime_minus_one_stream_cuda_contract_v0"
KERNEL_ID = "prime_minus_one_stream_cuda_kernel_v0"
HOST_RUNNER_ID = "prime_minus_one_cuda_host_runner_contract_v0"
HASH_ALGORITHM = "sha256_canonical_json_v1"

SYNTHETIC_MAPPING_ID = "stage5w-mapping-synthetic-prime-control-v0"
P56_BOUNDED_MAPPING_ID = "stage5w-mapping-p56-stage4o-bounded-v0"
FULL_P56_MAPPING_ID = "stage5w-mapping-p56-full-fixture-blocked-v0"

OUTPUT_DIR = Path("experiments/results/prime-minus-one-cuda-contract/stage5z")
CUDA_CONTRACT_PATH = Path("data/cuda/stage5z-prime-minus-one-cuda-contract.yaml")
KERNEL_ABI_PATH = Path("data/cuda/stage5z-prime-minus-one-cuda-kernel-abi.yaml")
HOST_RUNNER_CONTRACT_PATH = Path("data/cuda/stage5z-prime-minus-one-cuda-host-runner-contract.yaml")
BUFFER_CONTRACT_PATH = Path("data/cuda/stage5z-prime-minus-one-cuda-buffer-contract.yaml")
VALIDATION_VECTORS_PATH = Path("data/cuda/stage5z-prime-minus-one-cuda-validation-vectors.yaml")
FUTURE_PARITY_PLAN_PATH = Path("data/cuda/stage5z-prime-minus-one-cuda-future-parity-plan.yaml")
RESULT_STORE_COMPATIBILITY_PATH = Path("data/cuda/stage5z-prime-minus-one-cuda-result-store-compatibility.yaml")
FULL_P56_BLOCKER_PATH = Path("data/cuda/stage5z-prime-minus-one-cuda-full-p56-blocker.yaml")
SCORED_EXPERIMENT_DEFERRAL_PATH = Path("data/cuda/stage5z-prime-minus-one-scored-experiment-deferral.yaml")
IMPLEMENTATION_READINESS_PATH = Path("data/cuda/stage5z-prime-minus-one-cuda-implementation-readiness-gate.yaml")
NEXT_STAGE_DECISION_PATH = Path("data/cuda/stage5z-prime-minus-one-cuda-next-stage-decision.yaml")
SUMMARY_PATH = Path("data/cuda/stage5z-prime-minus-one-cuda-contract-summary.yaml")

STAGE5Y_SUMMARY_PATH = Path("data/cuda/stage5y-prime-minus-one-native-reporting-summary.yaml")
STAGE5Y_GATE_PATH = Path("data/cuda/stage5y-prime-minus-one-cuda-contract-readiness-gate.yaml")
STAGE5Y_SCORED_PATH = Path("data/cuda/stage5y-bounded-scored-experiment-readiness.yaml")
STAGE5X_PARITY_PATH = Path("data/cuda/stage5x-prime-minus-one-native-parity.yaml")
STAGE5W_MAPPING_PATH = Path("data/cuda/stage5w-prime-minus-one-candidate-batch-mapping.yaml")
STAGE5W_CONTRACT_PATH = Path("data/cuda/stage5w-prime-minus-one-stream-contract.yaml")
STAGE5U_ABI_PATH = Path("data/cuda/stage5u-candidate-batch-abi.yaml")
STAGE4P_SUMMARY_PATH = Path("data/research/stage4p-result-store-score-summary-unification-summary.yaml")

REPORT_FILES = {
    "cuda_contract": "cuda_contract_report.json",
    "kernel_abi": "kernel_abi_report.json",
    "host_runner": "host_runner_contract_report.json",
    "buffer_contract": "buffer_contract_report.json",
    "validation_vectors": "validation_vector_report.json",
    "future_parity": "future_parity_plan_report.json",
    "result_store": "result_store_compatibility_report.json",
    "full_p56_blocker": "full_p56_blocker_report.json",
    "scored_deferral": "scored_experiment_deferral_report.json",
    "implementation_gate": "implementation_readiness_gate.json",
    "next_stage": "next_stage_decision.json",
    "summary": "summary.json",
    "warnings": "warnings.jsonl",
}

EXPECTED_COUNTS = {
    "cuda_contract_records": 2,
    "kernel_abi_records": 1,
    "host_runner_contract_records": 1,
    "buffer_contract_records": 11,
    "validation_vector_records": 7,
    "future_parity_plan_records": 4,
    "result_store_compatibility_records": 2,
    "full_p56_blocker_records": 1,
    "scored_experiment_deferral_records": 6,
    "implementation_readiness_gate_records": 1,
    "next_stage_decision_records": 7,
}

SYNTHETIC_OUTPUT_HASH = "06a5c37f7e5eda8eec00cfab5b09faba6ec157488ca15f61a9189d4bf06005ab"
P56_BOUNDED_OUTPUT_HASH = "4a3059f12c0f8450bd4ef7e31bf879fbc104202e5fb0e53b7ba514241f07cd87"
P56_BOUNDED_FORMULA_HASH = "6034fe2431159615449db79c36869236d306768414038314d47d6d57d9ae7387"

COMMON_FALSE_FLAGS: dict[str, Any] = {
    "native_execution_performed": False,
    "python_reference_execution_performed": False,
    "native_cpu_execution_performed": False,
    "host_runner_implemented": False,
    "cuda_kernel_implemented": False,
    "cuda_execution_performed": False,
    "cuda_source_modified": False,
    "new_cuda_kernel_added": False,
    "new_cuda_kernels_added": 0,
    "device_kernel_arithmetic_modified": False,
    "gpu_benchmark_performed": False,
    "benchmark_execution_allowed": False,
    "performance_claim": False,
    "speedup_claim": False,
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
    "contract_preparation_only": True,
    "no_solve_claim": True,
    "no_gpu_ci_safe": True,
}

COMMON_RECORD_FLAGS: dict[str, Any] = {
    "stage_id": STAGE_ID,
    "source_stage_id": SOURCE_STAGE_ID,
    "candidate_batch_abi_id": ABI_ID,
    "source_native_contract_id": SOURCE_NATIVE_CONTRACT_ID,
    "cuda_contract_id": CUDA_CONTRACT_ID,
    "kernel_id": KERNEL_ID,
    **COMMON_FALSE_FLAGS,
    **COMMON_TRUE_FLAGS,
}

BAD_TRUE_FLAGS = tuple(COMMON_FALSE_FLAGS)

NEXT_STAGE_TITLE = "Stage 5AA - prime-minus-one CUDA synthetic kernel implementation and parity"
NEXT_STAGE_REASON = (
    "Stage 5Z completes a source-backed prime-minus-one CUDA contract, kernel ABI, host-runner "
    "boundary, buffer contract, and validation-vector plan without implementation. The next safe "
    "engineering step is a synthetic-only kernel implementation and parity stage, still excluding "
    "p56/full p56, unsolved pages, benchmarks, generated-body publication, and solve claims."
)


def base_record(record_type: str, schema: str, **extra: Any) -> dict[str, Any]:
    return {
        **COMMON_RECORD_FLAGS,
        "record_type": record_type,
        "schema": schema,
        **extra,
    }
