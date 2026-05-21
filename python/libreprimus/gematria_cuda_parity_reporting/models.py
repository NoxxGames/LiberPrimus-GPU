"""Constants for Stage 5K Gematria CUDA parity reporting records."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-5k"
NEXT_STAGE_WITH_BLOCKERS = (
    "Stage 5L - solved-fixture-safe Gematria shift_score token mapping "
    "and native parity fixture preparation"
)
NEXT_STAGE_EXECUTION = "Stage 5L - first solved-fixture-safe Gematria shift_score CUDA parity run"

IMPLEMENTED_KERNEL_NAME = "gematria_mod29_shift_score_kernel"
SOURCE_CONTRACT_ID = "gematria_mod29_shift_score_contract_v0"
SELECTED_FUTURE_KERNEL_ID = "shift_score_kernel"
NATIVE_FIXTURE_ID = "stage5h-gematria-mod29-synthetic-shift-fixture-v0"
NATIVE_FIXTURE_HASH = "a6d5d5161145fd31ab429a8e955e0412d7b0af6089f06ee8b33baf8cd00b27a0"
STAGE5F_SYNTHETIC_HASH = "76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66"
TOKEN_DOMAIN = "integers_0_to_28"
ARITHMETIC_DIRECTION = "forward_add_shift_mod29"
SEPARATOR_POLICY = "non_transformable_separators_preserved_unshifted"

OUTPUT_DIR = Path("experiments/results/gematria-cuda-parity-reporting/stage5k")
PARITY_REPORT_PATH = Path("data/cuda/stage5k-gematria-cuda-parity-report.yaml")
DEVICE_AUDIT_PATH = Path("data/cuda/stage5k-gematria-cuda-device-code-audit.yaml")
PREFLIGHT_PATH = Path("data/cuda/stage5k-gematria-solved-fixture-safe-preflight.yaml")
SCORE_PREFLIGHT_PATH = Path("data/cuda/stage5k-gematria-cuda-score-summary-preflight.yaml")
SUMMARY_PATH = Path("data/cuda/stage5k-gematria-cuda-parity-reporting-summary.yaml")

PARITY_REPORT_JSON = "parity_report.json"
DEVICE_AUDIT_JSON = "device_code_audit.json"
PREFLIGHT_JSON = "solved_fixture_safe_preflight.json"
SCORE_PREFLIGHT_JSON = "score_summary_preflight.json"
SUMMARY_JSON = "summary.json"
WARNINGS_JSONL = "warnings.jsonl"

PARITY_SCHEMA = Path("schemas/cuda/gematria-cuda-parity-report-record-v0.schema.json")
DEVICE_AUDIT_SCHEMA = Path("schemas/cuda/gematria-cuda-device-code-audit-record-v0.schema.json")
PREFLIGHT_SCHEMA = Path("schemas/cuda/gematria-solved-fixture-safe-preflight-record-v0.schema.json")
SCORE_PREFLIGHT_SCHEMA = Path("schemas/cuda/gematria-cuda-score-summary-preflight-record-v0.schema.json")
SUMMARY_SCHEMA = Path("schemas/cuda/stage5k-gematria-cuda-parity-reporting-summary-v0.schema.json")

STAGE5J_SUMMARY_PATH = Path("data/cuda/stage5j-gematria-cuda-kernel-summary.yaml")
STAGE5J_PARITY_PATH = Path("data/cuda/stage5j-gematria-cuda-synthetic-parity-records.yaml")
STAGE5H_MAPPING_PATH = Path("data/cuda/stage5h-gematria-solved-fixture-safe-mapping.yaml")
STAGE5H_SCORE_PLAN_PATH = Path("data/cuda/stage5h-gematria-score-summary-parity-plan.yaml")
STAGE4O_SOLVED_FIXTURE_MANIFEST = Path("experiments/manifests/cpu-batch/stage4o-solved-fixture-parity-batch.yaml")
STAGE4I_LABELS_PATH = Path("data/scoring/confidence-label-records-v0.yaml")

CUDA_SOURCE_PATHS = (
    Path("cuda/include/libreprimus/gematria_shift_score_kernel.cuh"),
    Path("cuda/kernels/gematria_shift_score_kernel.cu"),
    Path("cuda/include/libreprimus/shift_score_kernel.cuh"),
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
    "std::unique_ptr",
    "std::shared_ptr",
    "std::make_unique",
    "std::make_shared",
    "throw",
)

PREFLIGHT_BLOCKERS = (
    "need_exact_solved_fixture_token_domain_mapping_to_gematria_0_28_buffers",
    "need_host_side_result_record_shape_for_separator_and_token_kind_preservation",
    "need_output_token_hash_definition_for_solved_fixture_stream",
    "need_score_summary_parity_record_shape",
    "need_explicit_future_stage_approval",
    "need_no_unsolved_page_guardrail_recheck",
    "need_stage4o_parity_expectation_linkage",
)

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
    "separator_policy": SEPARATOR_POLICY,
    "synthetic_only": True,
    "new_cuda_kernel_added": False,
    "new_cuda_kernels_added": 0,
    "cuda_source_modified": False,
    "cuda_execution_performed": False,
    "solved_fixture_cuda_execution_allowed": False,
    "production_gematria_mod29_cuda_ready": False,
    "real_liber_primus_data_used": False,
    "solved_fixture_cuda_used": False,
    "unsolved_page_cuda_used": False,
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
    "stl_in_device_path_allowed": False,
    "no_solve_claim": True,
    "solve_claim": False,
}

BAD_TRUE_FLAGS = (
    "new_cuda_kernel_added",
    "cuda_source_modified",
    "cuda_execution_performed",
    "solved_fixture_cuda_execution_allowed",
    "production_gematria_mod29_cuda_ready",
    "real_liber_primus_data_used",
    "solved_fixture_cuda_used",
    "unsolved_page_cuda_used",
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
    "no_gpu_ci_safe",
    "python_semantic_reference_preserved",
    "no_solve_claim",
)
