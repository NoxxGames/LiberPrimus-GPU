"""Constants for Stage 5O Gematria CUDA repeat verification."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-5o"
PREVIOUS_EXECUTION_STAGE_ID = "stage-5m"
IMPLEMENTED_KERNEL_NAME = "gematria_mod29_shift_score_kernel"
EXECUTED_KERNEL = IMPLEMENTED_KERNEL_NAME
SOURCE_CONTRACT_ID = "gematria_mod29_shift_score_contract_v0"
EXECUTED_SEMANTICS = "gematria_shift_score_only"
TOKEN_DOMAIN = "integers_0_to_28"
ARITHMETIC_DIRECTION = "forward_add_shift_mod29"
ARITHMETIC_FORMULA = "(token + shift) % 29"
SEPARATOR_POLICY = "non_transformable_separators_preserved_unshifted"
HASH_ALGORITHM = "sha256_canonical_json_v1"
SCORE_SUMMARY_CONTRACT = "stage4i"
RESULT_STORE_CONTRACT = "stage4p"
ADDITIONAL_CUDA_EXECUTION_SCOPE = "exact_stage5m_repeat_only"

OUTPUT_DIR = Path("experiments/results/gematria-solved-fixture-cuda-repeat/stage5o")
BUILD_DIR = Path("build/stage5o-cuda")

STAGE5M_RUN_RECORDS = Path("data/cuda/stage5m-gematria-solved-fixture-cuda-run.yaml")
STAGE5M_PARITY_RECORDS = Path("data/cuda/stage5m-gematria-solved-fixture-cuda-parity.yaml")
STAGE5M_SUMMARY = Path("data/cuda/stage5m-solved-fixture-cuda-parity-summary.yaml")
STAGE5L_NATIVE_PARITY = Path("data/cuda/stage5l-gematria-solved-fixture-native-parity.yaml")
STAGE5N_SUMMARY = Path("data/cuda/stage5n-solved-fixture-cuda-reporting-summary.yaml")
STAGE4P_SUMMARY = Path("data/research/stage4p-result-store-score-summary-unification-summary.yaml")

REPEAT_RUN_PATH = Path("data/cuda/stage5o-gematria-solved-fixture-cuda-repeat-run.yaml")
REPEAT_PARITY_PATH = Path("data/cuda/stage5o-gematria-solved-fixture-cuda-repeat-parity.yaml")
RESULT_STORE_PREFLIGHT_PATH = Path("data/cuda/stage5o-gematria-cuda-result-store-preflight.yaml")
SCORE_SUMMARY_PREFLIGHT_PATH = Path("data/cuda/stage5o-gematria-cuda-score-summary-preflight.yaml")
EXPANSION_DECISION_PATH = Path("data/cuda/stage5o-gematria-cuda-expansion-decision.yaml")
SUMMARY_PATH = Path("data/cuda/stage5o-repeat-verification-result-store-summary.yaml")

REPEAT_RUN_REPORT = "repeat_run_report.json"
REPEAT_PARITY_REPORT = "repeat_parity_report.json"
RESULT_STORE_PREFLIGHT_REPORT = "result_store_preflight.json"
SCORE_SUMMARY_PREFLIGHT_REPORT = "score_summary_preflight.json"
EXPANSION_DECISION_REPORT = "expansion_decision.json"
SUMMARY_REPORT = "summary.json"
WARNINGS_REPORT = "warnings.jsonl"

REPEAT_RUN_SCHEMA = Path("schemas/cuda/gematria-solved-fixture-cuda-repeat-run-record-v0.schema.json")
REPEAT_PARITY_SCHEMA = Path("schemas/cuda/gematria-solved-fixture-cuda-repeat-parity-record-v0.schema.json")
RESULT_STORE_SCHEMA = Path("schemas/cuda/gematria-cuda-result-store-preflight-v0.schema.json")
SCORE_SUMMARY_SCHEMA = Path("schemas/cuda/gematria-cuda-score-summary-preflight-v0.schema.json")
EXPANSION_DECISION_SCHEMA = Path("schemas/cuda/gematria-cuda-expansion-decision-record-v0.schema.json")
SUMMARY_SCHEMA = Path("schemas/cuda/stage5o-repeat-verification-result-store-summary-v0.schema.json")

NEXT_STAGE_READY = "Stage 5P - controlled solved-fixture CUDA result-store integration"
NEXT_STAGE_TOOLCHAIN = "Stage 5O-followup - repeat CUDA toolchain repair and rerun"
NEXT_STAGE_MISMATCH = "Stage 5O-fix - repeat CUDA hash mismatch investigation"
NEXT_STAGE_PREFLIGHT = "Stage 5O-followup - result-store and score-summary preflight repair"

COMMON_POLICY_FLAGS = {
    "stage_id": STAGE_ID,
    "previous_execution_stage_id": PREVIOUS_EXECUTION_STAGE_ID,
    "implemented_kernel_name": IMPLEMENTED_KERNEL_NAME,
    "executed_kernel": EXECUTED_KERNEL,
    "source_contract_id": SOURCE_CONTRACT_ID,
    "executed_semantics": EXECUTED_SEMANTICS,
    "token_domain": TOKEN_DOMAIN,
    "arithmetic_direction": ARITHMETIC_DIRECTION,
    "arithmetic_formula": ARITHMETIC_FORMULA,
    "separator_policy": SEPARATOR_POLICY,
    "solved_fixture_cuda_execution_allowed": True,
    "solved_fixture_cuda_execution_scope": "exact_stage5l_mapped_token_buffers_only",
    "additional_cuda_execution_scope": ADDITIONAL_CUDA_EXECUTION_SCOPE,
    "unsolved_page_cuda_used": False,
    "real_liber_primus_cuda_data_used": False,
    "real_liber_primus_data_used": False,
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
    "ci_gpu_required": False,
    "no_gpu_ci_safe": True,
    "new_cuda_kernel_added": False,
    "new_cuda_kernels_added": 0,
    "cuda_source_modified": False,
    "device_kernel_arithmetic_modified": False,
    "cxx_launches_python_workers": False,
    "no_solve_claim": True,
    "solve_claim": False,
}

BAD_TRUE_FLAGS = (
    "unsolved_page_cuda_used",
    "real_liber_primus_cuda_data_used",
    "real_liber_primus_data_used",
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
    "ci_gpu_required",
    "new_cuda_kernel_added",
    "cuda_source_modified",
    "device_kernel_arithmetic_modified",
    "cxx_launches_python_workers",
    "solve_claim",
)

REQUIRED_TRUE_FLAGS = ("solved_fixture_cuda_execution_allowed", "no_gpu_ci_safe", "no_solve_claim")
