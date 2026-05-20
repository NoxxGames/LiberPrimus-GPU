"""Constants for Stage 5E CUDA kernel contract selection."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-5e"
NEXT_STAGE = "Stage 5F - first synthetic-only CUDA parity kernel implementation"
SELECTED_KERNEL_ID = "shift_score_kernel"
SELECTED_TARGET_ID = "stage5a-caesar_mod29-cuda-target"
SELECTED_TRANSFORM_FAMILY = "caesar_mod29"
SELECTED_ADAPTER_FAMILY = "native_cpu_synthetic_shift_adapter"
CONTRACT_ID = "stage5e-shift-score-first-kernel-contract"
ADAPTER_SELECTION_ID = "stage5e-caesar-mod29-adapter-selection"
NATIVE_PARITY_ADAPTER_ID = "stage5e-native-shift-parity-adapter-map"
READINESS_ID = "stage5e-shift-score-implementation-readiness"

OUTPUT_DIR = Path("experiments/results/cuda-kernel-contract/stage5e")
CONTRACT_REPORT = "first_kernel_contract_report.json"
ADAPTER_SELECTION_REPORT = "adapter_selection_report.json"
NATIVE_PARITY_REPORT = "native_parity_adapter_report.json"
READINESS_REPORT = "implementation_readiness_report.json"
SUMMARY_REPORT = "summary.json"
WARNINGS_REPORT = "warnings.jsonl"

CONTRACT_PATH = Path("data/cuda/stage5e-first-kernel-contract.yaml")
ADAPTER_SELECTION_PATH = Path("data/cuda/stage5e-cuda-adapter-selection.yaml")
NATIVE_PARITY_PATH = Path("data/cuda/stage5e-native-parity-adapter-map.yaml")
READINESS_PATH = Path("data/cuda/stage5e-implementation-readiness.yaml")
SUMMARY_PATH = Path("data/cuda/stage5e-first-kernel-contract-summary.yaml")

STAGE5A_TARGET_PLAN_PATH = Path("data/cuda/stage5a-cuda-target-plan.yaml")
STAGE5A_IMPLEMENTATION_GATES_PATH = Path("data/cuda/stage5a-cuda-implementation-gates.yaml")
STAGE5B_HARNESS_PATH = Path("data/cuda/stage5b-cuda-parity-harness-plan.yaml")
STAGE5B_FIXTURES_PATH = Path("data/cuda/stage5b-cuda-parity-fixtures.yaml")
STAGE5B_MATRIX_PATH = Path("data/cuda/stage5b-future-kernel-parity-matrix.yaml")
STAGE5D_SUMMARY_PATH = Path("data/native-cpu/stage5d-native-cpu-summary.yaml")
STAGE4O_SUMMARY_PATH = Path("data/research/stage4o-cpu-batch-adapter-expansion-summary.yaml")
STAGE4P_SUMMARY_PATH = Path("data/research/stage4p-result-store-score-summary-unification-summary.yaml")

CONTRACT_SCHEMA = Path("schemas/cuda/cuda-first-kernel-contract-record-v0.schema.json")
ADAPTER_SELECTION_SCHEMA = Path("schemas/cuda/cuda-adapter-selection-record-v0.schema.json")
NATIVE_PARITY_SCHEMA = Path("schemas/cuda/cuda-native-parity-adapter-record-v0.schema.json")
READINESS_SCHEMA = Path("schemas/cuda/cuda-implementation-readiness-record-v0.schema.json")
SUMMARY_SCHEMA = Path("schemas/cuda/stage5e-first-kernel-contract-summary-v0.schema.json")

BAD_TRUE_FLAGS = (
    "cuda_kernel_added",
    "cuda_source_modified",
    "cryptanalytic_cuda_kernel_added",
    "cuda_transform_executed",
    "gpu_benchmark_performed",
    "performance_claim",
    "speedup_claim",
    "broad_experiment_executed",
    "raw_data_processed",
    "solve_claim",
    "generated_outputs_committed",
    "codex_output_committed",
    "website_expansion",
    "cxx_launches_python_workers",
)

REQUIRED_FALSE_FLAGS = (
    *BAD_TRUE_FLAGS,
    "canonical_corpus_active",
    "page_boundaries_final",
    "cuda_required",
    "gpu_required",
    "local_16gb_profile_required",
)

COMMON_GUARDRAILS = {
    "cuda_kernel_contract_only": True,
    "cuda_kernel_added": False,
    "cuda_source_modified": False,
    "cryptanalytic_cuda_kernel_added": False,
    "cuda_transform_executed": False,
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
    "cuda_required": False,
    "gpu_required": False,
    "local_16gb_profile_required": False,
    "python_semantic_reference_preserved": True,
    "cxx_launches_python_workers": False,
}
