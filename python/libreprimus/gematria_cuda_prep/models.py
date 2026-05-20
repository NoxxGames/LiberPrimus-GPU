"""Constants for Stage 5I Gematria CUDA preparation records."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-5i"
NEXT_STAGE = "Stage 5J - Gematria mod-29 shift_score synthetic CUDA parity kernel implementation"

PREPARATION_ID = "stage5i-gematria-cuda-kernel-preparation-v0"
ABI_PLAN_ID = "stage5i-gematria-cuda-abi-plan-v0"
VALIDATION_VECTOR_ID = "stage5i-gematria-cuda-validation-vector-v0"
CHECKLIST_ID = "stage5i-gematria-cuda-implementation-checklist-v0"

SOURCE_CONTRACT_ID = "gematria_mod29_shift_score_contract_v0"
SELECTED_FUTURE_KERNEL_ID = "shift_score_kernel"
TARGET_FUTURE_KERNEL_NAME = "gematria_mod29_shift_score_kernel"
CURRENT_STAGE5F_KERNEL_SCOPE = "synthetic_uppercase_latin_only"
FUTURE_STAGE5J_SCOPE = "gematria_mod29_synthetic_numeric_cuda_parity_only"
TOKEN_DOMAIN = "integers_0_to_28"
ARITHMETIC_DIRECTION = "forward_add_shift_mod29"
ARITHMETIC_FORMULA = "(token + shift) % 29"
SEPARATOR_POLICY = "non_transformable_separators_preserved_unshifted"
NATIVE_FIXTURE_ID = "stage5h-gematria-mod29-synthetic-shift-fixture-v0"
NATIVE_FIXTURE_HASH = "a6d5d5161145fd31ab429a8e955e0412d7b0af6089f06ee8b33baf8cd00b27a0"
STAGE5F_HASH = "76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66"

FUTURE_KERNEL_HEADER = "cuda/include/libreprimus/gematria_shift_score_kernel.cuh"
FUTURE_KERNEL_SOURCE = "cuda/kernels/gematria_shift_score_kernel.cu"

OUTPUT_DIR = Path("experiments/results/gematria-cuda-prep/stage5i")
PREPARATION_PATH = Path("data/cuda/stage5i-gematria-cuda-kernel-preparation.yaml")
ABI_PLAN_PATH = Path("data/cuda/stage5i-gematria-cuda-abi-plan.yaml")
VALIDATION_VECTORS_PATH = Path("data/cuda/stage5i-gematria-cuda-validation-vectors.yaml")
CHECKLIST_PATH = Path("data/cuda/stage5i-gematria-cuda-implementation-checklist.yaml")
SUMMARY_PATH = Path("data/cuda/stage5i-gematria-cuda-preparation-summary.yaml")

KERNEL_PREPARATION_JSON = "kernel_preparation_report.json"
ABI_PLAN_JSON = "abi_plan_report.json"
VALIDATION_VECTORS_JSON = "validation_vectors_report.json"
IMPLEMENTATION_CHECKLIST_JSON = "implementation_checklist_report.json"
SUMMARY_JSON = "summary.json"
WARNINGS_JSONL = "warnings.jsonl"

PREPARATION_SCHEMA = Path("schemas/cuda/gematria-cuda-kernel-preparation-record-v0.schema.json")
ABI_PLAN_SCHEMA = Path("schemas/cuda/gematria-cuda-abi-plan-record-v0.schema.json")
VALIDATION_VECTOR_SCHEMA = Path("schemas/cuda/gematria-cuda-validation-vector-record-v0.schema.json")
CHECKLIST_SCHEMA = Path("schemas/cuda/gematria-cuda-implementation-checklist-record-v0.schema.json")
SUMMARY_SCHEMA = Path("schemas/cuda/stage5i-gematria-cuda-preparation-summary-v0.schema.json")

STAGE5H_CONTRACT_PATH = Path("data/cuda/stage5h-gematria-shift-score-contract.yaml")
STAGE5H_FIXTURES_PATH = Path("data/cuda/stage5h-gematria-native-parity-fixtures.yaml")
STAGE5G_AUDIT_PATH = Path("data/cuda/stage5g-cuda-device-code-subset-audit.yaml")
STAGE5F_SUMMARY_PATH = Path("data/cuda/stage5f-cuda-synthetic-kernel-summary.yaml")

COMMON_POLICY_FLAGS = {
    "stage_id": STAGE_ID,
    "source_contract_id": SOURCE_CONTRACT_ID,
    "selected_future_kernel_id": SELECTED_FUTURE_KERNEL_ID,
    "target_future_kernel_name": TARGET_FUTURE_KERNEL_NAME,
    "current_stage5f_kernel_scope": CURRENT_STAGE5F_KERNEL_SCOPE,
    "future_stage5j_scope": FUTURE_STAGE5J_SCOPE,
    "token_domain": TOKEN_DOMAIN,
    "arithmetic_direction": ARITHMETIC_DIRECTION,
    "separator_policy": SEPARATOR_POLICY,
    "native_fixture_id": NATIVE_FIXTURE_ID,
    "native_fixture_hash": NATIVE_FIXTURE_HASH,
    "stage5f_synthetic_hash": STAGE5F_HASH,
    "stage5f_hash_is_gematria_fixture_hash": False,
    "cuda_kernel_added": False,
    "new_cuda_kernel_added": False,
    "new_cuda_kernels_added": 0,
    "cuda_source_modified": False,
    "cuda_execution_performed": False,
    "gpu_benchmark_performed": False,
    "performance_claim": False,
    "speedup_claim": False,
    "real_liber_primus_data_used": False,
    "solved_fixture_cuda_used": False,
    "unsolved_page_cuda_used": False,
    "solved_fixture_cuda_execution_allowed": False,
    "production_gematria_mod29_cuda_ready": False,
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
    "cuda_kernel_added",
    "new_cuda_kernel_added",
    "cuda_source_modified",
    "cuda_execution_performed",
    "gpu_benchmark_performed",
    "performance_claim",
    "speedup_claim",
    "real_liber_primus_data_used",
    "solved_fixture_cuda_used",
    "unsolved_page_cuda_used",
    "solved_fixture_cuda_execution_allowed",
    "production_gematria_mod29_cuda_ready",
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
    "no_gpu_ci_safe",
    "python_semantic_reference_preserved",
    "device_code_subset_must_remain_compliant",
    "no_solve_claim",
)
