"""Constants for Stage 5R expanded solved-fixture-safe Gematria CUDA parity."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-5r"
SOURCE_STAGE_ID = "stage-5q"
IMPLEMENTED_KERNEL_NAME = "gematria_mod29_shift_score_kernel"
EXECUTED_KERNEL = IMPLEMENTED_KERNEL_NAME
SOURCE_CONTRACT_ID = "gematria_mod29_shift_score_contract_v0"
EXECUTED_SEMANTICS = "gematria_shift_score_only"
TOKEN_DOMAIN = "integers_0_to_28"
ARITHMETIC_DIRECTION = "forward_add_shift_mod29"
ARITHMETIC_FORMULA = "(token + shift) % 29"
SEPARATOR_POLICY = "non_transformable_separators_preserved_unshifted"
HASH_ALGORITHM = "sha256_canonical_json_v1"
RESULT_STORE_CONTRACT = "stage4p"
SCORE_SUMMARY_CONTRACT = "stage4i"
OUTPUT_ORDERING = "candidate-major"
APPROVED_SCOPE = "exact_three_stage5q_mapped_direct_translation_candidates_only"
EXPECTED_FIXTURE_IDS = ("p57-parable", "some-wisdom", "the-loss-of-divinity")

OUTPUT_DIR = Path("experiments/results/gematria-expanded-solved-fixture-cuda/stage5r")
BUILD_DIR = Path("build/stage5r-cuda")

STAGE5Q_CANDIDATE_INVENTORY = Path("data/cuda/stage5q-gematria-expansion-candidate-inventory.yaml")
STAGE5Q_TOKEN_MAPPING = Path("data/cuda/stage5q-gematria-expansion-token-mapping.yaml")
STAGE5Q_NATIVE_PARITY = Path("data/cuda/stage5q-gematria-expansion-native-parity.yaml")
STAGE5Q_RESULT_STORE_PREFLIGHT = Path("data/cuda/stage5q-gematria-expansion-result-store-preflight.yaml")
STAGE5Q_SUMMARY = Path("data/cuda/stage5q-expansion-candidate-mapping-summary.yaml")
STAGE4P_SUMMARY = Path("data/research/stage4p-result-store-score-summary-unification-summary.yaml")
STAGE4I_CONFIDENCE_LABELS = Path("data/scoring/confidence-label-records-v0.yaml")

RUN_RECORDS_PATH = Path("data/cuda/stage5r-gematria-expanded-solved-fixture-cuda-run.yaml")
PARITY_RECORDS_PATH = Path("data/cuda/stage5r-gematria-expanded-solved-fixture-cuda-parity.yaml")
BOUNDARY_RECORDS_PATH = Path("data/cuda/stage5r-gematria-expanded-solved-fixture-cuda-boundary.yaml")
RESULT_STORE_PREFLIGHT_PATH = Path("data/cuda/stage5r-gematria-expanded-solved-fixture-result-store-preflight.yaml")
SCORE_SUMMARY_PREFLIGHT_PATH = Path("data/cuda/stage5r-gematria-expanded-solved-fixture-score-summary-preflight.yaml")
SUMMARY_PATH = Path("data/cuda/stage5r-expanded-solved-fixture-cuda-parity-summary.yaml")

RUN_REPORT = "cuda_run_report.json"
PARITY_REPORT = "parity_report.json"
BOUNDARY_REPORT = "boundary_report.json"
RESULT_STORE_PREFLIGHT_REPORT = "result_store_preflight.json"
SCORE_SUMMARY_PREFLIGHT_REPORT = "score_summary_preflight.json"
SUMMARY_REPORT = "summary.json"
WARNINGS_REPORT = "warnings.jsonl"

RUN_SCHEMA = Path("schemas/cuda/gematria-expanded-solved-fixture-cuda-run-record-v0.schema.json")
PARITY_SCHEMA = Path("schemas/cuda/gematria-expanded-solved-fixture-cuda-parity-record-v0.schema.json")
BOUNDARY_SCHEMA = Path("schemas/cuda/gematria-expanded-solved-fixture-cuda-boundary-record-v0.schema.json")
RESULT_STORE_PREFLIGHT_SCHEMA = Path(
    "schemas/cuda/gematria-expanded-solved-fixture-result-store-preflight-record-v0.schema.json"
)
SCORE_SUMMARY_PREFLIGHT_SCHEMA = Path(
    "schemas/cuda/gematria-expanded-solved-fixture-score-summary-preflight-record-v0.schema.json"
)
SUMMARY_SCHEMA = Path("schemas/cuda/stage5r-expanded-solved-fixture-cuda-parity-summary-v0.schema.json")

NEXT_STAGE_READY = "Stage 5S - expanded solved-fixture Gematria CUDA parity reporting and result-store integration"
NEXT_STAGE_TOOLCHAIN = "Stage 5R-followup - expanded solved-fixture CUDA parity toolchain repair and rerun"
NEXT_STAGE_MISMATCH = "Stage 5R-fix - expanded solved-fixture Gematria CUDA parity mismatch investigation"
NEXT_STAGE_PARTIAL = "Stage 5R-followup - partial expanded solved-fixture CUDA parity gap closure"

COMMON_POLICY_FLAGS = {
    "stage_id": STAGE_ID,
    "source_stage_id": SOURCE_STAGE_ID,
    "implemented_kernel_name": IMPLEMENTED_KERNEL_NAME,
    "executed_kernel": EXECUTED_KERNEL,
    "source_contract_id": SOURCE_CONTRACT_ID,
    "executed_semantics": EXECUTED_SEMANTICS,
    "token_domain": TOKEN_DOMAIN,
    "arithmetic_direction": ARITHMETIC_DIRECTION,
    "arithmetic_formula": ARITHMETIC_FORMULA,
    "separator_policy": SEPARATOR_POLICY,
    "solved_fixture_cuda_execution_allowed": True,
    "solved_fixture_cuda_execution_scope": APPROVED_SCOPE,
    "approved_stage5r_scope": APPROVED_SCOPE,
    "consumed_controls_excluded": True,
    "blocked_original_family_fixtures_excluded": True,
    "original_transform_family_semantics_exercised": False,
    "new_cuda_kernel_added": False,
    "new_cuda_kernels_added": 0,
    "cuda_source_modified": False,
    "device_kernel_arithmetic_modified": False,
    "unsolved_page_cuda_used": False,
    "real_liber_primus_cuda_data_used": False,
    "real_liber_primus_data_used": False,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "gpu_benchmark_performed": False,
    "performance_claim": False,
    "speedup_claim": False,
    "performance_or_speedup_claims": False,
    "generated_body_publication_allowed": False,
    "generated_outputs_committed": False,
    "raw_data_processed": False,
    "codex_output_committed": False,
    "method_status_upgrade_allowed": False,
    "method_status_upgraded": False,
    "solve_claim": False,
    "no_solve_claim": True,
    "no_gpu_ci_safe": True,
    "local_16gb_profile_required": False,
    "ci_gpu_required": False,
    "cxx_launches_python_workers": False,
}

BAD_TRUE_FLAGS = (
    "new_cuda_kernel_added",
    "device_kernel_arithmetic_modified",
    "unsolved_page_cuda_used",
    "real_liber_primus_cuda_data_used",
    "real_liber_primus_data_used",
    "canonical_corpus_active",
    "page_boundaries_final",
    "gpu_benchmark_performed",
    "performance_claim",
    "speedup_claim",
    "performance_or_speedup_claims",
    "generated_body_publication_allowed",
    "generated_outputs_committed",
    "raw_data_processed",
    "codex_output_committed",
    "method_status_upgrade_allowed",
    "method_status_upgraded",
    "solve_claim",
    "local_16gb_profile_required",
    "ci_gpu_required",
    "cxx_launches_python_workers",
)

REQUIRED_TRUE_FLAGS = (
    "solved_fixture_cuda_execution_allowed",
    "consumed_controls_excluded",
    "blocked_original_family_fixtures_excluded",
    "no_solve_claim",
    "no_gpu_ci_safe",
)
