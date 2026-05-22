"""Constants for Stage 5X prime-minus-one native parity records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

STAGE_ID = "stage-5x"
SOURCE_STAGE_ID = "stage-5w"
ABI_ID = "candidate_batch_abi_v0"
CONTRACT_ID = "prime_minus_one_stream_native_contract_v0"
RESULT_SOURCE_KIND = "prime_minus_one_no_gpu_native_parity"
HASH_ALGORITHM = "sha256_canonical_json_v1"

SYNTHETIC_MAPPING_ID = "stage5w-mapping-synthetic-prime-control-v0"
P56_BOUNDED_MAPPING_ID = "stage5w-mapping-p56-stage4o-bounded-v0"
FULL_P56_MAPPING_ID = "stage5w-mapping-p56-full-fixture-blocked-v0"
P56_FIXTURE_ID = "p56-an-end-prime-minus-one"
P56_CANDIDATE_ID = "stage4o-prime-minus-one-an-v0"

OUTPUT_DIR = Path("experiments/results/prime-minus-one-native-parity/stage5x")
NATIVE_RUN_PATH = Path("data/cuda/stage5x-prime-minus-one-native-run.yaml")
NATIVE_PARITY_PATH = Path("data/cuda/stage5x-prime-minus-one-native-parity.yaml")
RESULT_STORE_PREFLIGHT_PATH = Path("data/cuda/stage5x-prime-minus-one-native-result-store-preflight.yaml")
SCORE_SUMMARY_PREFLIGHT_PATH = Path("data/cuda/stage5x-prime-minus-one-native-score-summary-preflight.yaml")
FULL_P56_BLOCKER_PATH = Path("data/cuda/stage5x-prime-minus-one-full-p56-blocker.yaml")
GUARDRAIL_PATH = Path("data/cuda/stage5x-prime-minus-one-native-guardrail.yaml")
NEXT_STAGE_DECISION_PATH = Path("data/cuda/stage5x-prime-minus-one-native-next-stage-decision.yaml")
SUMMARY_PATH = Path("data/cuda/stage5x-prime-minus-one-native-parity-summary.yaml")

STAGE5W_SUMMARY_PATH = Path("data/cuda/stage5w-prime-minus-one-native-contract-summary.yaml")
STAGE5W_MAPPING_PATH = Path("data/cuda/stage5w-prime-minus-one-candidate-batch-mapping.yaml")
STAGE5W_SCHEDULE_PATH = Path("data/cuda/stage5w-prime-minus-one-schedule.yaml")
STAGE5W_PREP_PATH = Path("data/cuda/stage5w-prime-minus-one-native-parity-preparation.yaml")
STAGE5L_TOKEN_MAPPING_PATH = Path("data/cuda/stage5l-gematria-solved-fixture-token-mapping.yaml")
STAGE5L_NATIVE_PARITY_PATH = Path("data/cuda/stage5l-gematria-solved-fixture-native-parity.yaml")

REPORT_FILES = {
    "native_run": "native_run_report.json",
    "native_parity": "native_parity_report.json",
    "result_store_preflight": "result_store_preflight_report.json",
    "score_summary_preflight": "score_summary_preflight_report.json",
    "full_p56_blocker": "full_p56_blocker_report.json",
    "guardrail": "guardrail_report.json",
    "next_stage": "next_stage_decision.json",
    "summary": "summary.json",
    "warnings": "warnings.jsonl",
}

COMMON_FALSE_FLAGS: dict[str, Any] = {
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

NEXT_STAGE_TITLE_READY = "Stage 5Y - prime-minus-one native parity reporting and CUDA contract readiness gate"
NEXT_STAGE_TITLE_FIX = "Stage 5X-fix - prime-minus-one native parity mismatch investigation"
NEXT_STAGE_REASON_READY = (
    "Both Stage 5W ready no-GPU mappings passed deterministic native parity, while full p56 "
    "fixture execution remains blocked pending a full committed token buffer. The next bounded "
    "stage can integrate compact reporting and decide whether CUDA contract preparation is ready."
)
