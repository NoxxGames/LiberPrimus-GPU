"""Constants for Stage 5F synthetic CUDA kernel records."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-5f"
NEXT_STAGE = "Stage 5G - shift_score CUDA parity reporting and solved-fixture-safe adapter preflight"

SELECTED_KERNEL_ID = "shift_score_kernel"
SELECTED_TARGET_ID = "stage5a-caesar_mod29-cuda-target"
SELECTED_TRANSFORM_FAMILY = "caesar_mod29"
SELECTED_ADAPTER_FAMILY = "native_cpu_synthetic_shift_adapter"
FIXTURE_ID = "stage5d-native-synthetic-shift-fixture-v0"
NATIVE_REFERENCE_HASH = "76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66"

OUTPUT_DIR = Path("experiments/results/cuda-kernel/stage5f")
BUILD_DIR = Path("build/stage5f-cuda")

IMPLEMENTATION_PATH = Path("data/cuda/stage5f-cuda-synthetic-kernel-implementation.yaml")
BUILD_RECORDS_PATH = Path("data/cuda/stage5f-cuda-kernel-build-records.yaml")
PARITY_RECORDS_PATH = Path("data/cuda/stage5f-cuda-synthetic-parity-records.yaml")
SUMMARY_PATH = Path("data/cuda/stage5f-cuda-synthetic-kernel-summary.yaml")

IMPLEMENTATION_REPORT = "kernel_implementation_report.json"
BUILD_REPORT = "kernel_build_report.json"
PARITY_REPORT = "synthetic_parity_report.json"
SUMMARY_REPORT = "summary.json"
WARNINGS_REPORT = "warnings.jsonl"

IMPLEMENTATION_SCHEMA = Path("schemas/cuda/cuda-synthetic-kernel-implementation-record-v0.schema.json")
BUILD_SCHEMA = Path("schemas/cuda/cuda-kernel-build-record-v0.schema.json")
PARITY_SCHEMA = Path("schemas/cuda/cuda-synthetic-parity-run-record-v0.schema.json")
SUMMARY_SCHEMA = Path("schemas/cuda/stage5f-synthetic-cuda-kernel-summary-v0.schema.json")

STAGE5E_CONTRACT_PATH = Path("data/cuda/stage5e-first-kernel-contract.yaml")
STAGE5E_SUMMARY_PATH = Path("data/cuda/stage5e-first-kernel-contract-summary.yaml")
STAGE5D_SUMMARY_PATH = Path("data/native-cpu/stage5d-native-cpu-summary.yaml")
STAGE5C_SUMMARY_PATH = Path("data/cuda/stage5c-cuda-build-device-summary.yaml")

COMMON_POLICY_FLAGS = {
    "selected_kernel_id": SELECTED_KERNEL_ID,
    "selected_target_id": SELECTED_TARGET_ID,
    "selected_transform_family": SELECTED_TRANSFORM_FAMILY,
    "selected_adapter_family": SELECTED_ADAPTER_FAMILY,
    "fixture_id": FIXTURE_ID,
    "synthetic_only": True,
    "real_liber_primus_data_used": False,
    "solved_fixture_cuda_used": False,
    "unsolved_page_cuda_used": False,
    "gpu_benchmark_performed": False,
    "performance_claim": False,
    "speedup_claim": False,
    "broad_experiment_executed": False,
    "raw_data_processed": False,
    "solve_claim": False,
    "no_solve_claim": True,
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
}

BAD_TRUE_FLAGS = (
    "real_liber_primus_data_used",
    "solved_fixture_cuda_used",
    "unsolved_page_cuda_used",
    "gpu_benchmark_performed",
    "performance_claim",
    "speedup_claim",
    "broad_experiment_executed",
    "raw_data_processed",
    "solve_claim",
    "generated_outputs_committed",
    "codex_output_committed",
    "website_expansion",
    "canonical_corpus_active",
    "page_boundaries_final",
    "local_16gb_profile_required",
    "ci_gpu_required",
    "cxx_launches_python_workers",
)

REQUIRED_TRUE_FLAGS = (
    "synthetic_only",
    "no_solve_claim",
    "no_gpu_ci_safe",
    "python_semantic_reference_preserved",
)
