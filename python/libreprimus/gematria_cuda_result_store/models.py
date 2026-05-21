"""Constants for Stage 5P Gematria CUDA result-store integration."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-5p"
SOURCE_STAGE_ID = "stage-5o"
IMPLEMENTED_KERNEL_NAME = "gematria_mod29_shift_score_kernel"
EXECUTED_KERNEL = IMPLEMENTED_KERNEL_NAME
SOURCE_CONTRACT_ID = "gematria_mod29_shift_score_contract_v0"
EXECUTED_SEMANTICS = "gematria_shift_score_only"
HASH_ALGORITHM = "sha256_canonical_json_v1"
RESULT_STORE_CONTRACT = "stage4p"
SCORE_SUMMARY_CONTRACT = "stage4i"
NEXT_STAGE_READY = "Stage 5Q - controlled solved-fixture-safe Gematria shift_score expansion candidate mapping"
NEXT_STAGE_PLANNING = "Stage 5Q - post-integration CUDA parity review and expansion planning"
NEXT_STAGE_BLOCKERS = "Stage 5Q - CUDA result-store integration blocker closure"
DEEP_RESEARCH_REVIEW = "Deep Research - Stage 5P CUDA parity integration and expansion review"

OUTPUT_DIR = Path("experiments/results/gematria-cuda-result-store/stage5p")

STAGE5O_REPEAT_PARITY = Path("data/cuda/stage5o-gematria-solved-fixture-cuda-repeat-parity.yaml")
STAGE5O_RESULT_STORE_PREFLIGHT = Path("data/cuda/stage5o-gematria-cuda-result-store-preflight.yaml")
STAGE5O_SCORE_SUMMARY_PREFLIGHT = Path("data/cuda/stage5o-gematria-cuda-score-summary-preflight.yaml")
STAGE5O_EXPANSION_DECISION = Path("data/cuda/stage5o-gematria-cuda-expansion-decision.yaml")
STAGE5O_SUMMARY = Path("data/cuda/stage5o-repeat-verification-result-store-summary.yaml")
STAGE4P_SUMMARY = Path("data/research/stage4p-result-store-score-summary-unification-summary.yaml")
STAGE4I_CONFIDENCE_LABELS = Path("data/scoring/confidence-label-records-v0.yaml")
METHOD_STATUS_RECORDS = Path("data/research/method-family-status-records-v0.yaml")

RESULT_STORE_INTEGRATION_PATH = Path("data/cuda/stage5p-gematria-cuda-result-store-integration.yaml")
SCORE_SUMMARY_INTEGRATION_PATH = Path("data/cuda/stage5p-gematria-cuda-score-summary-integration.yaml")
METHOD_STATUS_IMPACT_PATH = Path("data/cuda/stage5p-gematria-cuda-method-status-impact.yaml")
GENERATED_BODY_POLICY_PATH = Path("data/cuda/stage5p-gematria-cuda-generated-body-policy.yaml")
CONTROLLED_EXPANSION_CANDIDATES_PATH = Path("data/cuda/stage5p-gematria-controlled-expansion-candidates.yaml")
SUMMARY_PATH = Path("data/cuda/stage5p-cuda-result-store-integration-summary.yaml")

RESULT_STORE_INTEGRATION_REPORT = "result_store_integration_report.json"
SCORE_SUMMARY_INTEGRATION_REPORT = "score_summary_integration_report.json"
METHOD_STATUS_IMPACT_REPORT = "method_status_impact_report.json"
GENERATED_BODY_POLICY_REPORT = "generated_body_policy_report.json"
CONTROLLED_EXPANSION_CANDIDATE_REPORT = "controlled_expansion_candidate_report.json"
SUMMARY_REPORT = "summary.json"
WARNINGS_REPORT = "warnings.jsonl"

RESULT_STORE_INTEGRATION_SCHEMA = Path(
    "schemas/cuda/gematria-cuda-result-store-integration-record-v0.schema.json"
)
SCORE_SUMMARY_INTEGRATION_SCHEMA = Path(
    "schemas/cuda/gematria-cuda-score-summary-integration-record-v0.schema.json"
)
METHOD_STATUS_IMPACT_SCHEMA = Path("schemas/cuda/gematria-cuda-method-status-impact-record-v0.schema.json")
GENERATED_BODY_POLICY_SCHEMA = Path("schemas/cuda/gematria-cuda-generated-body-policy-record-v0.schema.json")
CONTROLLED_EXPANSION_CANDIDATE_SCHEMA = Path(
    "schemas/cuda/gematria-cuda-controlled-expansion-candidate-record-v0.schema.json"
)
SUMMARY_SCHEMA = Path("schemas/cuda/stage5p-cuda-result-store-integration-summary-v0.schema.json")

COMMON_POLICY_FLAGS = {
    "stage_id": STAGE_ID,
    "source_stage_id": SOURCE_STAGE_ID,
    "implemented_kernel_name": IMPLEMENTED_KERNEL_NAME,
    "executed_kernel": EXECUTED_KERNEL,
    "source_contract_id": SOURCE_CONTRACT_ID,
    "executed_semantics": EXECUTED_SEMANTICS,
    "compact_summary_only": True,
    "stage4p_compatibility": True,
    "stage4i_compatibility": True,
    "generated_body_publication_allowed": False,
    "generated_outputs_committed": False,
    "raw_data_processed": False,
    "codex_output_committed": False,
    "new_cuda_kernel_added": False,
    "new_cuda_kernels_added": 0,
    "cuda_source_modified": False,
    "device_kernel_arithmetic_modified": False,
    "cuda_execution_performed": False,
    "solved_fixture_cuda_used": False,
    "additional_cuda_execution_performed": False,
    "unsolved_page_cuda_used": False,
    "real_liber_primus_cuda_data_used": False,
    "real_liber_primus_data_used": False,
    "gpu_benchmark_performed": False,
    "performance_claim": False,
    "speedup_claim": False,
    "performance_or_speedup_claims": False,
    "broad_experiment_executed": False,
    "new_experiment_executed": False,
    "website_expansion": False,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "ci_gpu_required": False,
    "no_gpu_ci_safe": True,
    "local_16gb_profile_required": False,
    "cxx_launches_python_workers": False,
    "method_status_upgrade_allowed": False,
    "method_status_upgraded": False,
    "no_solve_claim": True,
    "solve_claim": False,
}

BAD_TRUE_FLAGS = (
    "generated_body_publication_allowed",
    "generated_outputs_committed",
    "raw_data_processed",
    "codex_output_committed",
    "new_cuda_kernel_added",
    "cuda_source_modified",
    "device_kernel_arithmetic_modified",
    "cuda_execution_performed",
    "solved_fixture_cuda_used",
    "additional_cuda_execution_performed",
    "unsolved_page_cuda_used",
    "real_liber_primus_cuda_data_used",
    "real_liber_primus_data_used",
    "gpu_benchmark_performed",
    "performance_claim",
    "speedup_claim",
    "performance_or_speedup_claims",
    "broad_experiment_executed",
    "new_experiment_executed",
    "website_expansion",
    "canonical_corpus_active",
    "page_boundaries_final",
    "ci_gpu_required",
    "local_16gb_profile_required",
    "cxx_launches_python_workers",
    "method_status_upgrade_allowed",
    "method_status_upgraded",
    "solve_claim",
)

REQUIRED_TRUE_FLAGS = ("compact_summary_only", "stage4p_compatibility", "stage4i_compatibility", "no_gpu_ci_safe", "no_solve_claim")
