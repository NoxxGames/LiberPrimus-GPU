"""Constants for Stage 5S expanded CUDA parity reporting."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-5s"
SOURCE_STAGE_ID = "stage-5r"
SOURCE_STAGE5Q = "stage-5q"
RESULT_SOURCE_KIND = "expanded_solved_fixture_safe_cuda_parity"
IMPLEMENTED_KERNEL_NAME = "gematria_mod29_shift_score_kernel"
EXECUTED_KERNEL = IMPLEMENTED_KERNEL_NAME
SOURCE_CONTRACT_ID = "gematria_mod29_shift_score_contract_v0"
EXECUTED_SEMANTICS = "gematria_shift_score_only"
HASH_ALGORITHM = "sha256_canonical_json_v1"
RESULT_STORE_CONTRACT = "stage4p"
SCORE_SUMMARY_CONTRACT = "stage4i"
APPROVED_SCOPE = "exact_three_stage5q_mapped_direct_translation_candidates_only"
CONFIDENCE_LABEL = "scoring_not_available"
CONFIDENCE_INTERPRETATION = "triage_only"
NEXT_DEEP_RESEARCH_PROMPT = "Deep Research - Stage 5M-5S CUDA parity arc project review and next-direction assessment"
NEXT_DEEP_RESEARCH_REASON = (
    "Stage 5S integration succeeded after synthetic parity, exact solved-fixture parity, repeat verification, "
    "compact result-store integration, candidate mapping, and expanded parity; remaining choices are strategic."
)

OUTPUT_DIR = Path("experiments/results/gematria-expanded-cuda-result-store/stage5s")

STAGE5R_SUMMARY = Path("data/cuda/stage5r-expanded-solved-fixture-cuda-parity-summary.yaml")
STAGE5R_RUN = Path("data/cuda/stage5r-gematria-expanded-solved-fixture-cuda-run.yaml")
STAGE5R_PARITY = Path("data/cuda/stage5r-gematria-expanded-solved-fixture-cuda-parity.yaml")
STAGE5R_BOUNDARY = Path("data/cuda/stage5r-gematria-expanded-solved-fixture-cuda-boundary.yaml")
STAGE5R_RESULT_STORE_PREFLIGHT = Path("data/cuda/stage5r-gematria-expanded-solved-fixture-result-store-preflight.yaml")
STAGE5R_SCORE_SUMMARY_PREFLIGHT = Path("data/cuda/stage5r-gematria-expanded-solved-fixture-score-summary-preflight.yaml")
STAGE5Q_CANDIDATE_INVENTORY = Path("data/cuda/stage5q-gematria-expansion-candidate-inventory.yaml")
STAGE5P_SUMMARY = Path("data/cuda/stage5p-cuda-result-store-integration-summary.yaml")
STAGE4P_SUMMARY = Path("data/research/stage4p-result-store-score-summary-unification-summary.yaml")
STAGE4I_CONFIDENCE_LABELS = Path("data/scoring/confidence-label-records-v0.yaml")

PARITY_REPORT_PATH = Path("data/cuda/stage5s-gematria-expanded-cuda-parity-report.yaml")
RESULT_STORE_INTEGRATION_PATH = Path("data/cuda/stage5s-gematria-expanded-cuda-result-store-integration.yaml")
SCORE_SUMMARY_INTEGRATION_PATH = Path("data/cuda/stage5s-gematria-expanded-cuda-score-summary-integration.yaml")
METHOD_STATUS_IMPACT_PATH = Path("data/cuda/stage5s-gematria-expanded-cuda-method-status-impact.yaml")
GENERATED_BODY_POLICY_PATH = Path("data/cuda/stage5s-gematria-expanded-cuda-generated-body-policy.yaml")
BOUNDARY_REVIEW_PATH = Path("data/cuda/stage5s-gematria-expanded-cuda-boundary-review.yaml")
NEXT_STEP_DECISION_PATH = Path("data/cuda/stage5s-gematria-expanded-cuda-next-step-decision.yaml")
SUMMARY_PATH = Path("data/cuda/stage5s-expanded-cuda-result-store-integration-summary.yaml")

PARITY_REPORT_JSON = "parity_report.json"
RESULT_STORE_REPORT_JSON = "result_store_integration_report.json"
SCORE_SUMMARY_REPORT_JSON = "score_summary_integration_report.json"
METHOD_STATUS_REPORT_JSON = "method_status_impact_report.json"
GENERATED_BODY_POLICY_REPORT_JSON = "generated_body_policy_report.json"
BOUNDARY_REVIEW_REPORT_JSON = "boundary_review_report.json"
NEXT_STEP_DECISION_JSON = "controlled_next_step_decision.json"
SUMMARY_JSON = "summary.json"
WARNINGS_JSONL = "warnings.jsonl"

COMMON_FLAGS = {
    "stage_id": STAGE_ID,
    "source_stage_id": SOURCE_STAGE_ID,
    "result_source_kind": RESULT_SOURCE_KIND,
    "compact_summary_only": True,
    "generated_body_publication_allowed": False,
    "generated_outputs_committed": False,
    "raw_data_processed": False,
    "codex_output_committed": False,
    "new_cuda_kernel_added": False,
    "new_cuda_kernels_added": 0,
    "cuda_source_modified": False,
    "cuda_execution_performed": False,
    "additional_cuda_execution_performed": False,
    "unsolved_page_cuda_used": False,
    "real_liber_primus_cuda_data_used": False,
    "solved_fixture_cuda_used": False,
    "gpu_benchmark_performed": False,
    "performance_claim": False,
    "speedup_claim": False,
    "method_status_upgrade_allowed": False,
    "method_status_upgraded": False,
    "solve_claim": False,
    "no_solve_claim": True,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "no_gpu_ci_safe": True,
    "local_16gb_profile_required": False,
    "ci_gpu_required": False,
    "cxx_launches_python_workers": False,
}

BAD_TRUE_FLAGS = (
    "generated_body_publication_allowed",
    "generated_outputs_committed",
    "raw_data_processed",
    "codex_output_committed",
    "new_cuda_kernel_added",
    "cuda_source_modified",
    "cuda_execution_performed",
    "additional_cuda_execution_performed",
    "unsolved_page_cuda_used",
    "real_liber_primus_cuda_data_used",
    "solved_fixture_cuda_used",
    "gpu_benchmark_performed",
    "performance_claim",
    "speedup_claim",
    "method_status_upgrade_allowed",
    "method_status_upgraded",
    "solve_claim",
    "canonical_corpus_active",
    "page_boundaries_final",
    "local_16gb_profile_required",
    "ci_gpu_required",
    "cxx_launches_python_workers",
)

EXPECTED_FIXTURES = ("p57-parable", "some-wisdom", "the-loss-of-divinity")
