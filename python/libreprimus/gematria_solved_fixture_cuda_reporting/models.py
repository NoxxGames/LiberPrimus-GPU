"""Constants for Stage 5N solved-fixture-safe Gematria CUDA reporting."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-5n"
PREVIOUS_STAGE_ID = "stage-5m"
IMPLEMENTED_KERNEL_NAME = "gematria_mod29_shift_score_kernel"
EXECUTED_SEMANTICS = "gematria_shift_score_only"
HASH_ALGORITHM = "sha256_canonical_json_v1"
SCORE_SUMMARY_CONTRACT = "stage4i"
RESULT_STORE_CONTRACT = "stage4p"

OUTPUT_DIR = Path("experiments/results/gematria-solved-fixture-cuda-reporting/stage5n")
STAGE5M_RUN_RECORDS = Path("data/cuda/stage5m-gematria-solved-fixture-cuda-run.yaml")
STAGE5M_PARITY_RECORDS = Path("data/cuda/stage5m-gematria-solved-fixture-cuda-parity.yaml")
STAGE5M_BOUNDARY_RECORDS = Path("data/cuda/stage5m-gematria-solved-fixture-cuda-boundaries.yaml")
STAGE5M_SUMMARY = Path("data/cuda/stage5m-solved-fixture-cuda-parity-summary.yaml")
STAGE4P_SUMMARY = Path("data/research/stage4p-result-store-score-summary-unification-summary.yaml")

PARITY_REPORT_PATH = Path("data/cuda/stage5n-gematria-solved-fixture-cuda-report.yaml")
CONTROLLED_EXPANSION_GATE_PATH = Path("data/cuda/stage5n-gematria-controlled-expansion-gate.yaml")
BOUNDARY_REVIEW_PATH = Path("data/cuda/stage5n-gematria-cuda-boundary-review.yaml")
RESULT_STORE_PREFLIGHT_PATH = Path("data/cuda/stage5n-gematria-cuda-result-store-preflight.yaml")
NO_UNSOLVED_GUARDRAIL_PATH = Path("data/cuda/stage5n-gematria-no-unsolved-guardrail.yaml")
SUMMARY_PATH = Path("data/cuda/stage5n-solved-fixture-cuda-reporting-summary.yaml")

PARITY_REPORT_JSON = "parity_report.json"
CONTROLLED_EXPANSION_GATE_JSON = "controlled_expansion_gate.json"
BOUNDARY_REVIEW_JSON = "boundary_review.json"
RESULT_STORE_PREFLIGHT_JSON = "result_store_preflight.json"
NO_UNSOLVED_GUARDRAIL_JSON = "no_unsolved_guardrail.json"
SUMMARY_JSON = "summary.json"
WARNINGS_JSONL = "warnings.jsonl"

PARITY_SCHEMA = Path("schemas/cuda/gematria-solved-fixture-cuda-report-record-v0.schema.json")
GATE_SCHEMA = Path("schemas/cuda/gematria-cuda-controlled-expansion-gate-record-v0.schema.json")
BOUNDARY_SCHEMA = Path("schemas/cuda/gematria-cuda-boundary-review-record-v0.schema.json")
RESULT_STORE_SCHEMA = Path("schemas/cuda/gematria-cuda-result-store-preflight-record-v0.schema.json")
NO_UNSOLVED_SCHEMA = Path("schemas/cuda/gematria-no-unsolved-guardrail-record-v0.schema.json")
SUMMARY_SCHEMA = Path("schemas/cuda/stage5n-solved-fixture-cuda-reporting-summary-v0.schema.json")

NEXT_STAGE = "Stage 5O - solved-fixture-safe Gematria CUDA repeat verification and result-store preflight"
NEXT_STAGE_REASON = (
    "Stage 5M exact parity passed, but Stage 5N only approves exact-repeat reporting and "
    "result-store preflight; broader solved-fixture and unsolved CUDA remain blocked."
)

COMMON_FALSE_FLAGS = {
    "additional_cuda_execution_performed": False,
    "cuda_execution_performed": False,
    "solved_fixture_cuda_used": False,
    "unsolved_page_cuda_used": False,
    "real_liber_primus_cuda_data_used": False,
    "real_liber_primus_data_used": False,
    "new_cuda_kernel_added": False,
    "new_cuda_kernels_added": 0,
    "cuda_source_modified": False,
    "device_kernel_arithmetic_modified": False,
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
    "cxx_launches_python_workers": False,
    "solve_claim": False,
}

COMMON_TRUE_FLAGS = {
    "no_gpu_ci_safe": True,
    "no_solve_claim": True,
}

BAD_TRUE_FLAGS = tuple(key for key, value in COMMON_FALSE_FLAGS.items() if value is False)
GATE_STATUSES = (
    "approved_for_exact_repeat_only",
    "needs_candidate_selection",
    "needs_result_store_preflight",
    "needs_score_summary_preflight",
    "needs_source_mapping",
    "blocked_broad_scope",
    "blocked_unsolved",
    "blocked_pending_deep_review",
    "blocked_pending_explicit_approval",
)
