"""Constants for Stage 5G CUDA parity reporting records."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-5g"
NEXT_STAGE = "Stage 5H - Gematria mod-29 shift_score contract and native parity fixture preparation"

SELECTED_KERNEL_ID = "shift_score_kernel"
SELECTED_TARGET_ID = "stage5a-caesar_mod29-cuda-target"
SELECTED_TRANSFORM_FAMILY = "caesar_mod29"
SELECTED_ADAPTER_FAMILY = "native_cpu_synthetic_shift_adapter"
FIXTURE_ID = "stage5d-native-synthetic-shift-fixture-v0"
NATIVE_REFERENCE_HASH = "76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66"

OUTPUT_DIR = Path("experiments/results/cuda-parity-reporting/stage5g")
PARITY_REPORT_PATH = Path("data/cuda/stage5g-shift-score-parity-report.yaml")
DEVICE_AUDIT_PATH = Path("data/cuda/stage5g-cuda-device-code-subset-audit.yaml")
PREFLIGHT_PATH = Path("data/cuda/stage5g-solved-fixture-safe-adapter-preflight.yaml")
SUMMARY_PATH = Path("data/cuda/stage5g-cuda-parity-reporting-summary.yaml")

PARITY_REPORT_JSON = "shift_score_parity_report.json"
DEVICE_AUDIT_JSON = "device_code_subset_audit.json"
PREFLIGHT_JSON = "solved_fixture_safe_preflight.json"
SUMMARY_JSON = "summary.json"
WARNINGS_JSONL = "warnings.jsonl"

PARITY_SCHEMA = Path("schemas/cuda/cuda-shift-score-parity-report-record-v0.schema.json")
DEVICE_AUDIT_SCHEMA = Path("schemas/cuda/cuda-device-code-subset-audit-record-v0.schema.json")
PREFLIGHT_SCHEMA = Path("schemas/cuda/cuda-solved-fixture-safe-preflight-record-v0.schema.json")
SUMMARY_SCHEMA = Path("schemas/cuda/stage5g-cuda-parity-reporting-summary-v0.schema.json")

STAGE5F_SUMMARY_PATH = Path("data/cuda/stage5f-cuda-synthetic-kernel-summary.yaml")
STAGE5F_PARITY_PATH = Path("data/cuda/stage5f-cuda-synthetic-parity-records.yaml")
STAGE5E_SUMMARY_PATH = Path("data/cuda/stage5e-first-kernel-contract-summary.yaml")
STAGE5D_SUMMARY_PATH = Path("data/native-cpu/stage5d-native-cpu-summary.yaml")

CUDA_SOURCE_PATHS = (
    Path("cuda/include/libreprimus/cuda_smoke.cuh"),
    Path("cuda/include/libreprimus/shift_score_kernel.cuh"),
    Path("cuda/kernels/cuda_smoke.cu"),
    Path("cuda/kernels/shift_score_kernel.cu"),
)

BANNED_CUDA_TOKENS = (
    "<array>",
    "<vector>",
    "<string>",
    "<span>",
    "<optional>",
    "<variant>",
    "<sstream>",
    "<iomanip>",
    "<iostream>",
    "std::array",
    "std::vector",
    "std::string",
    "std::span",
    "std::optional",
    "std::variant",
    "std::ostringstream",
    "std::cout",
    "std::cerr",
    "throw",
)

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
    "cuda_kernel_added": False,
    "new_cuda_kernel_added": False,
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
    "cuda_kernel_added",
    "new_cuda_kernel_added",
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
