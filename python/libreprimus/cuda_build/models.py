"""Constants for Stage 5C CUDA build/device detection records."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-5c"

STAGE5C_OUTPUT_DIR = Path("experiments/results/cuda-build/stage5c")
BUILD_PROFILES_PATH = Path("data/cuda/stage5c-cuda-build-profiles.yaml")
TOOLCHAIN_PATH = Path("data/cuda/stage5c-cuda-toolchain-detection.yaml")
DEVICE_PATH = Path("data/cuda/stage5c-cuda-device-detection.yaml")
SMOKE_BUILD_PATH = Path("data/cuda/stage5c-cuda-smoke-build-records.yaml")
SUMMARY_PATH = Path("data/cuda/stage5c-cuda-build-device-summary.yaml")

BUILD_PROFILE_SCHEMA = Path("schemas/cuda/cuda-build-profile-record-v0.schema.json")
TOOLCHAIN_SCHEMA = Path("schemas/cuda/cuda-toolchain-detection-record-v0.schema.json")
DEVICE_SCHEMA = Path("schemas/cuda/cuda-device-detection-record-v0.schema.json")
SMOKE_BUILD_SCHEMA = Path("schemas/cuda/cuda-smoke-build-record-v0.schema.json")
SUMMARY_SCHEMA = Path("schemas/cuda/stage5c-cuda-build-device-summary-v0.schema.json")

TOOLCHAIN_REPORT = "toolchain_detection_report.json"
DEVICE_REPORT = "device_detection_report.json"
SMOKE_BUILD_REPORT = "smoke_build_report.json"
SUMMARY_REPORT = "summary.json"
WARNINGS_JSONL = "warnings.jsonl"

CUDA_BUILD_POLICY = {
    "cuda_build_device_detection_only": True,
    "cuda_required": False,
    "gpu_required": False,
    "local_16gb_profile_required": False,
    "compatibility_8gb_profile_present": True,
    "cuda_kernel_added": False,
    "cuda_source_modified": False,
    "cryptanalytic_cuda_kernel_added": False,
    "gpu_benchmark_performed": False,
    "performance_claim": False,
    "speedup_claim": False,
    "broad_experiment_executed": False,
    "raw_data_processed": False,
    "solve_claim": False,
    "no_solve_claim": True,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "generated_outputs_committed": False,
    "codex_output_committed": False,
    "website_expansion": False,
}

BAD_TRUE_FLAGS = (
    "cuda_required",
    "gpu_required",
    "local_16gb_profile_required",
    "cuda_kernel_added",
    "cuda_source_modified",
    "cryptanalytic_cuda_kernel_added",
    "gpu_benchmark_performed",
    "performance_claim",
    "speedup_claim",
    "broad_experiment_executed",
    "raw_data_processed",
    "solve_claim",
    "canonical_corpus_active",
    "page_boundaries_final",
    "generated_outputs_committed",
    "codex_output_committed",
    "website_expansion",
)
