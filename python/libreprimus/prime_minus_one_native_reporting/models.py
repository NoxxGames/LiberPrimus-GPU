"""Constants for Stage 5Y prime-minus-one native reporting records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

STAGE_ID = "stage-5y"
SOURCE_STAGE_ID = "stage-5x"
SOURCE_CONTRACT_STAGE_ID = "stage-5w"
ABI_ID = "candidate_batch_abi_v0"
CONTRACT_ID = "prime_minus_one_stream_native_contract_v0"
HASH_ALGORITHM = "sha256_canonical_json_v1"

SYNTHETIC_MAPPING_ID = "stage5w-mapping-synthetic-prime-control-v0"
P56_BOUNDED_MAPPING_ID = "stage5w-mapping-p56-stage4o-bounded-v0"
FULL_P56_MAPPING_ID = "stage5w-mapping-p56-full-fixture-blocked-v0"

OUTPUT_DIR = Path("experiments/results/prime-minus-one-native-reporting/stage5y")
PARITY_REPORT_PATH = Path("data/cuda/stage5y-prime-minus-one-native-parity-report.yaml")
RESULT_STORE_INTEGRATION_PATH = Path("data/cuda/stage5y-prime-minus-one-native-result-store-integration.yaml")
SCORE_SUMMARY_INTEGRATION_PATH = Path("data/cuda/stage5y-prime-minus-one-native-score-summary-integration.yaml")
METHOD_STATUS_IMPACT_PATH = Path("data/cuda/stage5y-prime-minus-one-native-method-status-impact.yaml")
GENERATED_BODY_POLICY_PATH = Path("data/cuda/stage5y-prime-minus-one-generated-body-policy.yaml")
FULL_P56_BLOCKER_PRESERVATION_PATH = Path("data/cuda/stage5y-prime-minus-one-full-p56-blocker-preservation.yaml")
CUDA_CONTRACT_READINESS_PATH = Path("data/cuda/stage5y-prime-minus-one-cuda-contract-readiness-gate.yaml")
SCORED_EXPERIMENT_READINESS_PATH = Path("data/cuda/stage5y-bounded-scored-experiment-readiness.yaml")
GUARDRAIL_PATH = Path("data/cuda/stage5y-prime-minus-one-native-reporting-guardrail.yaml")
NEXT_STAGE_DECISION_PATH = Path("data/cuda/stage5y-prime-minus-one-native-reporting-next-stage-decision.yaml")
SUMMARY_PATH = Path("data/cuda/stage5y-prime-minus-one-native-reporting-summary.yaml")

STAGE5X_SUMMARY_PATH = Path("data/cuda/stage5x-prime-minus-one-native-parity-summary.yaml")
STAGE5X_RUN_PATH = Path("data/cuda/stage5x-prime-minus-one-native-run.yaml")
STAGE5X_PARITY_PATH = Path("data/cuda/stage5x-prime-minus-one-native-parity.yaml")
STAGE5X_RESULT_STORE_PREFLIGHT_PATH = Path("data/cuda/stage5x-prime-minus-one-native-result-store-preflight.yaml")
STAGE5X_SCORE_SUMMARY_PREFLIGHT_PATH = Path("data/cuda/stage5x-prime-minus-one-native-score-summary-preflight.yaml")
STAGE5X_FULL_P56_BLOCKER_PATH = Path("data/cuda/stage5x-prime-minus-one-full-p56-blocker.yaml")
STAGE5W_SUMMARY_PATH = Path("data/cuda/stage5w-prime-minus-one-native-contract-summary.yaml")
STAGE5W_MAPPING_PATH = Path("data/cuda/stage5w-prime-minus-one-candidate-batch-mapping.yaml")
STAGE4P_SUMMARY_PATH = Path("data/research/stage4p-result-store-score-summary-unification-summary.yaml")

REPORT_FILES = {
    "parity_report": "native_parity_report.json",
    "result_store": "result_store_integration_report.json",
    "score_summary": "score_summary_integration_report.json",
    "method_status": "method_status_impact_report.json",
    "generated_body_policy": "generated_body_policy_report.json",
    "full_p56_blocker": "full_p56_blocker_report.json",
    "cuda_contract": "cuda_contract_readiness_gate.json",
    "scored_experiment": "scored_experiment_readiness_report.json",
    "guardrail": "guardrail_report.json",
    "next_stage": "next_stage_decision.json",
    "summary": "summary.json",
    "warnings": "warnings.jsonl",
}

COMMON_FALSE_FLAGS: dict[str, Any] = {
    "native_execution_performed": False,
    "python_reference_execution_performed": False,
    "native_cpu_execution_performed": False,
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
    "reporting_only": True,
    "no_solve_claim": True,
    "no_gpu_ci_safe": True,
}

COMMON_RECORD_FLAGS: dict[str, Any] = {
    "stage_id": STAGE_ID,
    "source_stage_id": SOURCE_STAGE_ID,
    "candidate_batch_abi_id": ABI_ID,
    "contract_id": CONTRACT_ID,
    **COMMON_FALSE_FLAGS,
    **COMMON_TRUE_FLAGS,
}

BAD_TRUE_FLAGS = tuple(COMMON_FALSE_FLAGS)

NEXT_STAGE_TITLE = "Stage 5Z - prime-minus-one CUDA contract preparation"
NEXT_STAGE_REASON = (
    "Stage 5Y compact reporting integrated the two Stage 5X hash-matched no-GPU "
    "native parity mappings, preserved the full-p56 blocker, and kept CUDA execution, "
    "kernel implementation, and benchmarking blocked. The next bounded engineering "
    "step can prepare a prime-minus-one CUDA contract without implementing a kernel."
)
