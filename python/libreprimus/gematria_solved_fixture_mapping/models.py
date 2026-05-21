"""Constants for Stage 5L solved-fixture-safe Gematria token mapping."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-5l"
IMPLEMENTED_KERNEL_NAME = "gematria_mod29_shift_score_kernel"
SOURCE_CONTRACT_ID = "gematria_mod29_shift_score_contract_v0"
SELECTED_FUTURE_KERNEL_ID = "shift_score_kernel"
TOKEN_DOMAIN = "integers_0_to_28"
TOKEN_DOMAIN_MIN = 0
TOKEN_DOMAIN_MAX = 28
ARITHMETIC_DIRECTION = "forward_add_shift_mod29"
ARITHMETIC_FORMULA = "(token + shift) % 29"
SEPARATOR_POLICY = "non_transformable_separators_preserved_unshifted"
OUTPUT_ORDERING = "candidate-major"
HASH_ALGORITHM = "sha256_canonical_json_v1"
SCORE_SUMMARY_CONTRACT = "stage4i"

CANDIDATE_SHIFTS = (0, 1, 3, 13, 28)
ALLOWED_CONFIDENCE_LABELS = (
    "positive_control_like",
    "strong_lead",
    "moderate_lead",
    "weak_lead",
    "low_signal",
    "noise_like",
    "negative_control_like",
    "scoring_not_available",
    "calibration_not_available",
)

OUTPUT_DIR = Path("experiments/results/gematria-solved-fixture-mapping/stage5l")
TOKEN_MAPPING_PATH = Path("data/cuda/stage5l-gematria-solved-fixture-token-mapping.yaml")
NATIVE_PARITY_PATH = Path("data/cuda/stage5l-gematria-solved-fixture-native-parity.yaml")
OUTPUT_HASH_CONTRACT_PATH = Path(
    "data/cuda/stage5l-gematria-solved-fixture-output-hash-contract.yaml"
)
SCORE_SUMMARY_SHAPE_PATH = Path(
    "data/cuda/stage5l-gematria-solved-fixture-score-summary-shape.yaml"
)
SUMMARY_PATH = Path("data/cuda/stage5l-solved-fixture-token-mapping-summary.yaml")

TOKEN_MAPPING_JSON = "token_mapping_report.json"
NATIVE_PARITY_JSON = "native_parity_report.json"
OUTPUT_HASH_CONTRACT_JSON = "output_hash_contract_report.json"
SCORE_SUMMARY_SHAPE_JSON = "score_summary_shape_report.json"
SUMMARY_JSON = "summary.json"
WARNINGS_JSONL = "warnings.jsonl"

TOKEN_MAPPING_SCHEMA = Path(
    "schemas/cuda/gematria-solved-fixture-token-mapping-record-v0.schema.json"
)
NATIVE_PARITY_SCHEMA = Path(
    "schemas/cuda/gematria-solved-fixture-native-parity-record-v0.schema.json"
)
OUTPUT_HASH_CONTRACT_SCHEMA = Path(
    "schemas/cuda/gematria-solved-fixture-output-hash-contract-v0.schema.json"
)
SCORE_SUMMARY_SHAPE_SCHEMA = Path(
    "schemas/cuda/gematria-solved-fixture-score-summary-shape-v0.schema.json"
)
SUMMARY_SCHEMA = Path("schemas/cuda/stage5l-solved-fixture-token-mapping-summary-v0.schema.json")

STAGE5K_PREFLIGHT_PATH = Path("data/cuda/stage5k-gematria-solved-fixture-safe-preflight.yaml")
STAGE5H_CONTRACT_PATH = Path("data/cuda/stage5h-gematria-shift-score-contract.yaml")
STAGE5H_SCORE_PLAN_PATH = Path("data/cuda/stage5h-gematria-score-summary-parity-plan.yaml")
STAGE4O_SOLVED_FIXTURE_MANIFEST = Path(
    "experiments/manifests/cpu-batch/stage4o-solved-fixture-parity-batch.yaml"
)

BLOCKERS_BEFORE = (
    "need_exact_solved_fixture_token_domain_mapping_to_gematria_0_28_buffers",
    "need_explicit_future_stage_approval",
    "need_host_side_result_record_shape_for_separator_and_token_kind_preservation",
    "need_no_unsolved_page_guardrail_recheck",
    "need_output_token_hash_definition_for_solved_fixture_stream",
    "need_score_summary_parity_record_shape",
    "need_stage4o_parity_expectation_linkage",
)
RESOLVABLE_BLOCKERS = tuple(blocker for blocker in BLOCKERS_BEFORE if blocker != "need_explicit_future_stage_approval")
REMAINING_APPROVAL_BLOCKER = "need_explicit_future_stage_approval"

NEXT_STAGE_EXECUTION = "Stage 5M - first solved-fixture-safe Gematria shift_score CUDA parity run"
NEXT_STAGE_TOKEN_GAP = "Stage 5M - solved-fixture-safe Gematria token-source gap closure"
NEXT_STAGE_BLOCKER_CLOSURE = "Stage 5M - solved-fixture-safe Gematria CUDA parity blocker closure"

BAD_TRUE_FLAGS = (
    "new_cuda_kernel_added",
    "cuda_source_modified",
    "cuda_execution_performed",
    "solved_fixture_cuda_execution_allowed",
    "production_gematria_mod29_cuda_ready",
    "real_liber_primus_cuda_data_used",
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
    "solve_claim",
)
REQUIRED_TRUE_FLAGS = ("no_gpu_ci_safe", "python_semantic_reference_preserved", "no_solve_claim")

COMMON_POLICY_FLAGS = {
    "stage_id": STAGE_ID,
    "implemented_kernel_name": IMPLEMENTED_KERNEL_NAME,
    "source_contract_id": SOURCE_CONTRACT_ID,
    "selected_future_kernel_id": SELECTED_FUTURE_KERNEL_ID,
    "token_domain": TOKEN_DOMAIN,
    "arithmetic_direction": ARITHMETIC_DIRECTION,
    "arithmetic_formula": ARITHMETIC_FORMULA,
    "separator_policy": SEPARATOR_POLICY,
    "new_cuda_kernel_added": False,
    "new_cuda_kernels_added": 0,
    "cuda_source_modified": False,
    "cuda_execution_performed": False,
    "solved_fixture_cuda_execution_allowed": False,
    "production_gematria_mod29_cuda_ready": False,
    "real_liber_primus_cuda_data_used": False,
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
    "no_solve_claim": True,
    "solve_claim": False,
}
