"""Constants for Stage 5T CUDA solved-family readiness records."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-5t"
SOURCE_STAGE_ID = "stage-5s"
RESULT_SOURCE_KIND = "cuda_solved_family_readiness_matrix"
OUTPUT_DIR = Path("experiments/results/cuda-solved-family-readiness/stage5t")

FIXTURE_ROOT = Path("data/fixtures/solved-pages")
TRANSFORM_REGISTRY = Path("data/transform-registry/cpu-reference-transforms-v0.json")
STAGE5S_SUMMARY = Path("data/cuda/stage5s-expanded-cuda-result-store-integration-summary.yaml")
STAGE5S_PARITY = Path("data/cuda/stage5s-gematria-expanded-cuda-parity-report.yaml")
STAGE5R_SUMMARY = Path("data/cuda/stage5r-expanded-solved-fixture-cuda-parity-summary.yaml")
STAGE5M_SUMMARY = Path("data/cuda/stage5m-solved-fixture-cuda-parity-summary.yaml")
STAGE5O_SUMMARY = Path("data/cuda/stage5o-repeat-verification-result-store-summary.yaml")

INVENTORY_PATH = Path("data/cuda/stage5t-solved-family-cuda-inventory.yaml")
PARITY_MATRIX_PATH = Path("data/cuda/stage5t-solved-family-cuda-parity-matrix.yaml")
KERNEL_READINESS_PATH = Path("data/cuda/stage5t-cuda-kernel-readiness.yaml")
BATCH_ABI_GAPS_PATH = Path("data/cuda/stage5t-cuda-candidate-batch-abi-gaps.yaml")
BENCHMARK_READINESS_PATH = Path("data/cuda/stage5t-cuda-benchmark-readiness.yaml")
NO_UNSOLVED_GUARDRAIL_PATH = Path("data/cuda/stage5t-cuda-no-unsolved-guardrail-review.yaml")
NEXT_STAGE_DECISION_PATH = Path("data/cuda/stage5t-cuda-next-stage-decision.yaml")
SUMMARY_PATH = Path("data/cuda/stage5t-cuda-solved-family-readiness-summary.yaml")

INVENTORY_REPORT_JSON = "solved_family_inventory_report.json"
PARITY_MATRIX_REPORT_JSON = "cuda_parity_matrix_report.json"
KERNEL_READINESS_REPORT_JSON = "kernel_readiness_report.json"
BATCH_ABI_GAP_REPORT_JSON = "batch_abi_gap_report.json"
BENCHMARK_READINESS_REPORT_JSON = "benchmark_readiness_report.json"
NO_UNSOLVED_GUARDRAIL_REPORT_JSON = "no_unsolved_guardrail_report.json"
NEXT_STAGE_DECISION_JSON = "next_stage_decision.json"
SUMMARY_JSON = "summary.json"
WARNINGS_JSONL = "warnings.jsonl"

IMPLEMENTED_KERNEL_NAME = "gematria_mod29_shift_score_kernel"
SHIFT_SCORE_CONTRACT = "gematria_mod29_shift_score_contract_v0"
NEXT_STAGE_TITLE = "Stage 5U - unified candidate batch ABI and backend contract consolidation"
NEXT_STAGE_REASON = (
    "Multiple solved families now have CPU references or native token-buffer references, but original "
    "transform families need shared batch ABI surfaces for token buffers, key schedules, stream schedules, "
    "score vectors, and top-k outputs before another CUDA kernel contract is responsible."
)

COMMON_FLAGS = {
    "stage_id": STAGE_ID,
    "source_stage_id": SOURCE_STAGE_ID,
    "result_source_kind": RESULT_SOURCE_KIND,
    "deep_research_review_consumed": True,
    "metadata_only": True,
    "compact_summary_only": True,
    "cuda_execution_performed": False,
    "cuda_source_modified": False,
    "new_cuda_kernel_added": False,
    "new_cuda_kernels_added": 0,
    "device_kernel_arithmetic_modified": False,
    "gpu_benchmark_performed": False,
    "performance_claim": False,
    "speedup_claim": False,
    "unsolved_page_cuda_used": False,
    "real_liber_primus_cuda_data_used": False,
    "solved_fixture_cuda_used": False,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "generated_body_publication_allowed": False,
    "generated_outputs_committed": False,
    "raw_data_processed": False,
    "codex_output_committed": False,
    "method_status_upgrade_allowed": False,
    "method_status_upgraded": False,
    "solve_claim": False,
    "no_solve_claim": True,
    "no_gpu_ci_safe": True,
    "ci_gpu_required": False,
    "local_16gb_profile_required": False,
    "cxx_launches_python_workers": False,
}

BAD_TRUE_FLAGS = tuple(
    key
    for key, value in COMMON_FLAGS.items()
    if value is False
    and key
    not in {
        "metadata_only",
        "compact_summary_only",
        "no_solve_claim",
        "no_gpu_ci_safe",
        "deep_research_review_consumed",
    }
)
