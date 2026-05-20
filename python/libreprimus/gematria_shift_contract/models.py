"""Constants for Stage 5H Gematria mod-29 shift_score contract records."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-5h"
NEXT_STAGE = "Stage 5I - Gematria mod-29 shift_score synthetic CUDA parity kernel preparation"

CONTRACT_ID = "gematria_mod29_shift_score_contract_v0"
FIXTURE_ID = "stage5h-gematria-mod29-synthetic-shift-fixture-v0"
SCORE_PLAN_ID = "stage5h-gematria-score-summary-parity-plan-v0"
SELECTED_FUTURE_KERNEL_ID = "shift_score_kernel"
CURRENT_STAGE5F_KERNEL_SCOPE = "synthetic_uppercase_latin_only"
PRODUCTION_CONTRACT_SCOPE = "numeric_gematria_mod29_tokens"
TOKEN_DOMAIN = "integers_0_to_28"
ARITHMETIC_DIRECTION = "forward_add_shift_mod29"
ARITHMETIC_FORMULA = "(token + shift) % 29"
SEPARATOR_POLICY = "non_transformable_separators_preserved_unshifted"
OUTPUT_ORDERING = "candidate_index_order"
STAGE5F_HASH = "76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66"

OUTPUT_DIR = Path("experiments/results/gematria-shift-contract/stage5h")
CONTRACT_PATH = Path("data/cuda/stage5h-gematria-shift-score-contract.yaml")
FIXTURES_PATH = Path("data/cuda/stage5h-gematria-native-parity-fixtures.yaml")
MAPPING_PATH = Path("data/cuda/stage5h-gematria-solved-fixture-safe-mapping.yaml")
SCORE_PLAN_PATH = Path("data/cuda/stage5h-gematria-score-summary-parity-plan.yaml")
SUMMARY_PATH = Path("data/cuda/stage5h-gematria-shift-contract-summary.yaml")

CONTRACT_JSON = "contract_report.json"
FIXTURE_JSON = "native_fixture_report.json"
MAPPING_JSON = "solved_fixture_mapping_report.json"
SCORE_PLAN_JSON = "score_summary_parity_plan.json"
SUMMARY_JSON = "summary.json"
WARNINGS_JSONL = "warnings.jsonl"

CONTRACT_SCHEMA = Path("schemas/cuda/gematria-shift-score-contract-record-v0.schema.json")
FIXTURE_SCHEMA = Path("schemas/cuda/gematria-native-parity-fixture-record-v0.schema.json")
MAPPING_SCHEMA = Path("schemas/cuda/gematria-solved-fixture-safe-mapping-record-v0.schema.json")
SCORE_PLAN_SCHEMA = Path("schemas/cuda/gematria-score-summary-parity-plan-record-v0.schema.json")
SUMMARY_SCHEMA = Path("schemas/cuda/stage5h-gematria-shift-contract-summary-v0.schema.json")

STAGE4O_SOLVED_FIXTURE_MANIFEST = Path("experiments/manifests/cpu-batch/stage4o-solved-fixture-parity-batch.yaml")

COMMON_POLICY_FLAGS = {
    "stage_id": STAGE_ID,
    "selected_future_kernel_id": SELECTED_FUTURE_KERNEL_ID,
    "current_stage5f_kernel_scope": CURRENT_STAGE5F_KERNEL_SCOPE,
    "production_contract_scope": PRODUCTION_CONTRACT_SCOPE,
    "gematria_mod29_contract_defined": True,
    "stage5h_cuda_execution_allowed": False,
    "solved_fixture_cuda_execution_allowed": False,
    "production_gematria_mod29_cuda_ready": False,
    "real_liber_primus_data_used": False,
    "solved_fixture_cuda_used": False,
    "unsolved_page_cuda_used": False,
    "cuda_kernel_added": False,
    "new_cuda_kernel_added": False,
    "new_cuda_kernels_added": 0,
    "cuda_source_modified": False,
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
    "device_code_subset_must_remain_compliant": True,
}

BAD_TRUE_FLAGS = (
    "stage5h_cuda_execution_allowed",
    "solved_fixture_cuda_execution_allowed",
    "production_gematria_mod29_cuda_ready",
    "real_liber_primus_data_used",
    "solved_fixture_cuda_used",
    "unsolved_page_cuda_used",
    "cuda_kernel_added",
    "new_cuda_kernel_added",
    "cuda_source_modified",
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
    "gematria_mod29_contract_defined",
    "no_solve_claim",
    "no_gpu_ci_safe",
    "python_semantic_reference_preserved",
    "device_code_subset_must_remain_compliant",
)

PREFLIGHT_BLOCKERS = (
    "need_gematria_fixture_native_parity_accepted",
    "need_explicit_token_domain_mapping_from_solved_fixture_stream_to_0_28_rune_tokens",
    "need_separator_handling_declaration",
    "need_stage4o_parity_expectation_linkage",
    "need_score_summary_parity_plan",
    "need_no_unsolved_page_guardrails",
    "need_explicit_future_stage_approval",
)
