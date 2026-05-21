"""Constants for Stage 5M solved-fixture-safe Gematria CUDA parity."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-5m"
IMPLEMENTED_KERNEL_NAME = "gematria_mod29_shift_score_kernel"
EXECUTED_KERNEL = IMPLEMENTED_KERNEL_NAME
SOURCE_CONTRACT_ID = "gematria_mod29_shift_score_contract_v0"
EXECUTED_SEMANTICS = "gematria_shift_score_only"
TOKEN_DOMAIN = "integers_0_to_28"
ARITHMETIC_DIRECTION = "forward_add_shift_mod29"
ARITHMETIC_FORMULA = "(token + shift) % 29"
SEPARATOR_POLICY = "non_transformable_separators_preserved_unshifted"
HASH_ALGORITHM = "sha256_canonical_json_v1"
SCORE_SUMMARY_CONTRACT = "stage4i"
OUTPUT_ORDERING = "candidate-major"

OUTPUT_DIR = Path("experiments/results/gematria-solved-fixture-cuda/stage5m")
BUILD_DIR = Path("build/stage5m-cuda")
RUN_RECORDS_PATH = Path("data/cuda/stage5m-gematria-solved-fixture-cuda-run.yaml")
PARITY_RECORDS_PATH = Path("data/cuda/stage5m-gematria-solved-fixture-cuda-parity.yaml")
BOUNDARY_RECORDS_PATH = Path("data/cuda/stage5m-gematria-solved-fixture-cuda-boundaries.yaml")
SUMMARY_PATH = Path("data/cuda/stage5m-solved-fixture-cuda-parity-summary.yaml")

TOKEN_MAPPING_PATH = Path("data/cuda/stage5l-gematria-solved-fixture-token-mapping.yaml")
NATIVE_PARITY_PATH = Path("data/cuda/stage5l-gematria-solved-fixture-native-parity.yaml")
STAGE5L_SUMMARY_PATH = Path("data/cuda/stage5l-solved-fixture-token-mapping-summary.yaml")

RUN_REPORT = "cuda_run_report.json"
PARITY_REPORT = "parity_report.json"
BOUNDARY_REPORT = "boundary_report.json"
SUMMARY_REPORT = "summary.json"
WARNINGS_REPORT = "warnings.jsonl"

RUN_SCHEMA = Path("schemas/cuda/gematria-solved-fixture-cuda-run-record-v0.schema.json")
PARITY_SCHEMA = Path("schemas/cuda/gematria-solved-fixture-cuda-parity-record-v0.schema.json")
BOUNDARY_SCHEMA = Path("schemas/cuda/gematria-solved-fixture-cuda-boundary-record-v0.schema.json")
SUMMARY_SCHEMA = Path("schemas/cuda/stage5m-solved-fixture-cuda-parity-summary-v0.schema.json")

RUN_STATUSES = (
    "pending",
    "passed",
    "failed",
    "skipped_not_requested",
    "skipped_missing_cuda",
    "skipped_build_not_passed",
    "skipped_executable_missing",
    "failed_environment",
    "failed_toolkit_resolution",
)
BUILD_STATUSES = (
    "pending",
    "passed",
    "skipped_not_requested",
    "skipped_missing_cuda",
    "failed_environment",
    "failed_toolkit_resolution",
    "failed",
)
PARITY_STATUSES = (
    "passed",
    "failed_hash_mismatch",
    "failed_cuda_run",
    "skipped_missing_cuda",
    "skipped_not_requested",
    "skipped_build_not_passed",
    "skipped_executable_missing",
    "unknown",
)

NEXT_STAGE_READY = "Stage 5N - solved-fixture-safe Gematria CUDA parity reporting and controlled expansion gate"
NEXT_STAGE_TOOLCHAIN = "Stage 5M-followup - solved-fixture-safe CUDA parity toolchain repair and rerun"
NEXT_STAGE_MISMATCH = "Stage 5M-fix - solved-fixture-safe Gematria CUDA parity mismatch investigation"
NEXT_STAGE_PARTIAL = "Stage 5M-followup - partial solved-fixture-safe Gematria CUDA parity gap closure"

COMMON_POLICY_FLAGS = {
    "stage_id": STAGE_ID,
    "implemented_kernel_name": IMPLEMENTED_KERNEL_NAME,
    "executed_kernel": EXECUTED_KERNEL,
    "source_contract_id": SOURCE_CONTRACT_ID,
    "executed_semantics": EXECUTED_SEMANTICS,
    "token_domain": TOKEN_DOMAIN,
    "arithmetic_direction": ARITHMETIC_DIRECTION,
    "arithmetic_formula": ARITHMETIC_FORMULA,
    "separator_policy": SEPARATOR_POLICY,
    "solved_fixture_cuda_execution_allowed": True,
    "solved_fixture_cuda_execution_scope": "exact_stage5l_mapped_token_buffers_only",
    "unsolved_page_cuda_used": False,
    "real_liber_primus_cuda_data_used": False,
    "real_liber_primus_data_used": False,
    "gpu_benchmark_performed": False,
    "performance_claim": False,
    "speedup_claim": False,
    "performance_or_speedup_claims": False,
    "broad_experiment_executed": False,
    "raw_data_processed": False,
    "generated_outputs_committed": False,
    "codex_output_committed": False,
    "website_expansion": False,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "ci_gpu_required": False,
    "no_gpu_ci_safe": True,
    "new_cuda_kernel_added": False,
    "new_cuda_kernels_added": 0,
    "device_kernel_arithmetic_modified": False,
    "cxx_launches_python_workers": False,
    "no_solve_claim": True,
    "solve_claim": False,
}

BAD_TRUE_FLAGS = (
    "unsolved_page_cuda_used",
    "real_liber_primus_cuda_data_used",
    "real_liber_primus_data_used",
    "gpu_benchmark_performed",
    "performance_claim",
    "speedup_claim",
    "performance_or_speedup_claims",
    "broad_experiment_executed",
    "raw_data_processed",
    "generated_outputs_committed",
    "codex_output_committed",
    "website_expansion",
    "canonical_corpus_active",
    "page_boundaries_final",
    "ci_gpu_required",
    "new_cuda_kernel_added",
    "device_kernel_arithmetic_modified",
    "cxx_launches_python_workers",
    "solve_claim",
)

REQUIRED_TRUE_FLAGS = (
    "solved_fixture_cuda_execution_allowed",
    "no_gpu_ci_safe",
    "no_solve_claim",
)
