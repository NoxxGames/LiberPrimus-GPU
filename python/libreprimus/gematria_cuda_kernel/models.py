"""Constants for Stage 5J Gematria CUDA kernel records."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-5j"
NEXT_STAGE_IF_PASSED = "Stage 5K - Gematria shift_score CUDA parity reporting and solved-fixture-safe preflight"
NEXT_STAGE_IF_UNVERIFIED = "Stage 5J-followup - CUDA toolkit/build repair and Gematria synthetic parity verification"

IMPLEMENTED_KERNEL_NAME = "gematria_mod29_shift_score_kernel"
SOURCE_CONTRACT_ID = "gematria_mod29_shift_score_contract_v0"
SELECTED_FUTURE_KERNEL_ID = "shift_score_kernel"
TOKEN_DOMAIN = "integers_0_to_28"
ARITHMETIC_DIRECTION = "forward_add_shift_mod29"
ARITHMETIC_FORMULA = "(token + shift) % 29"
SEPARATOR_POLICY = "non_transformable_separators_preserved_unshifted"
NATIVE_FIXTURE_ID = "stage5h-gematria-mod29-synthetic-shift-fixture-v0"
NATIVE_FIXTURE_HASH = "a6d5d5161145fd31ab429a8e955e0412d7b0af6089f06ee8b33baf8cd00b27a0"
STAGE5F_SYNTHETIC_HASH = "76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66"

INPUT_TOKEN_VALUES = (0, 1, 0, 28, 13, 0, 5)
TRANSFORMABLE_MASK = (1, 1, 0, 1, 1, 0, 1)
TOKEN_KINDS = ("rune", "rune", "word_separator", "rune", "rune", "clause_separator", "rune")
SHIFTS = (0, 1, 3, 13, 28)
EXPECTED_OUTPUTS = (
    (0, 1, 0, 28, 13, 0, 5),
    (1, 2, 0, 0, 14, 0, 6),
    (3, 4, 0, 2, 16, 0, 8),
    (13, 14, 0, 12, 26, 0, 18),
    (28, 0, 0, 27, 12, 0, 4),
)

OUTPUT_DIR = Path("experiments/results/gematria-cuda-kernel/stage5j")
BUILD_DIR = Path("build/stage5j-cuda")

IMPLEMENTATION_PATH = Path("data/cuda/stage5j-gematria-cuda-kernel-implementation.yaml")
BUILD_RECORDS_PATH = Path("data/cuda/stage5j-gematria-cuda-kernel-build-records.yaml")
PARITY_RECORDS_PATH = Path("data/cuda/stage5j-gematria-cuda-synthetic-parity-records.yaml")
SUMMARY_PATH = Path("data/cuda/stage5j-gematria-cuda-kernel-summary.yaml")

IMPLEMENTATION_REPORT = "kernel_implementation_report.json"
BUILD_REPORT = "kernel_build_report.json"
PARITY_REPORT = "synthetic_parity_report.json"
SUMMARY_REPORT = "summary.json"
WARNINGS_REPORT = "warnings.jsonl"

IMPLEMENTATION_SCHEMA = Path("schemas/cuda/gematria-cuda-kernel-implementation-record-v0.schema.json")
BUILD_SCHEMA = Path("schemas/cuda/gematria-cuda-kernel-build-record-v0.schema.json")
PARITY_SCHEMA = Path("schemas/cuda/gematria-cuda-synthetic-parity-record-v0.schema.json")
SUMMARY_SCHEMA = Path("schemas/cuda/stage5j-gematria-cuda-kernel-summary-v0.schema.json")

KERNEL_HEADER = "cuda/include/libreprimus/gematria_shift_score_kernel.cuh"
KERNEL_SOURCE = "cuda/kernels/gematria_shift_score_kernel.cu"
KERNEL_TEST = "cuda/tests/gematria_shift_score_kernel_test.cpp"
STAGE5F_HEADER = "cuda/include/libreprimus/shift_score_kernel.cuh"
STAGE5F_SOURCE = "cuda/kernels/shift_score_kernel.cu"

COMMON_POLICY_FLAGS = {
    "stage_id": STAGE_ID,
    "implemented_kernel_name": IMPLEMENTED_KERNEL_NAME,
    "source_contract_id": SOURCE_CONTRACT_ID,
    "selected_future_kernel_id": SELECTED_FUTURE_KERNEL_ID,
    "native_fixture_id": NATIVE_FIXTURE_ID,
    "native_fixture_hash": NATIVE_FIXTURE_HASH,
    "stage5f_synthetic_hash": STAGE5F_SYNTHETIC_HASH,
    "stage5f_hash_is_gematria_fixture_hash": False,
    "token_domain": TOKEN_DOMAIN,
    "arithmetic_direction": ARITHMETIC_DIRECTION,
    "arithmetic_formula": ARITHMETIC_FORMULA,
    "separator_policy": SEPARATOR_POLICY,
    "synthetic_only": True,
    "cuda_kernel_added": True,
    "new_cuda_kernel_added": True,
    "new_cuda_kernels_added": 1,
    "cuda_source_modified": True,
    "real_liber_primus_data_used": False,
    "solved_fixture_cuda_used": False,
    "unsolved_page_cuda_used": False,
    "solved_fixture_cuda_execution_allowed": False,
    "production_gematria_mod29_cuda_ready": False,
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
    "local_16gb_profile_required": False,
    "ci_gpu_required": False,
    "no_gpu_ci_safe": True,
    "python_semantic_reference_preserved": True,
    "cxx_launches_python_workers": False,
    "device_code_subset_must_remain_compliant": True,
    "stl_in_device_path_allowed": False,
    "no_solve_claim": True,
    "solve_claim": False,
}

BAD_TRUE_FLAGS = (
    "real_liber_primus_data_used",
    "solved_fixture_cuda_used",
    "unsolved_page_cuda_used",
    "solved_fixture_cuda_execution_allowed",
    "production_gematria_mod29_cuda_ready",
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
    "local_16gb_profile_required",
    "ci_gpu_required",
    "cxx_launches_python_workers",
    "stl_in_device_path_allowed",
    "solve_claim",
)

REQUIRED_TRUE_FLAGS = (
    "synthetic_only",
    "cuda_kernel_added",
    "new_cuda_kernel_added",
    "cuda_source_modified",
    "no_gpu_ci_safe",
    "python_semantic_reference_preserved",
    "device_code_subset_must_remain_compliant",
    "no_solve_claim",
)

BUILD_STATUSES = (
    "passed",
    "skipped_not_requested",
    "skipped_missing_cuda",
    "failed_missing_cuda",
    "failed_environment",
    "failed_toolkit_resolution",
    "failed",
)

PARITY_STATUSES = (
    "passed",
    "skipped_build_not_passed",
    "skipped_build_not_requested",
    "skipped_missing_cuda",
    "skipped_executable_missing",
    "failed",
)
