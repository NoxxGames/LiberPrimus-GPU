"""Constants for Stage 5B CUDA parity harness records."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-5b"

STAGE5B_OUTPUT_DIR = Path("experiments/results/cuda-parity/stage5b")
HARNESS_PLAN_PATH = Path("data/cuda/stage5b-cuda-parity-harness-plan.yaml")
PARITY_FIXTURES_PATH = Path("data/cuda/stage5b-cuda-parity-fixtures.yaml")
BACKEND_CAPABILITY_PATH = Path("data/cuda/stage5b-cuda-backend-capability.yaml")
FUTURE_KERNEL_MATRIX_PATH = Path("data/cuda/stage5b-future-kernel-parity-matrix.yaml")
SUMMARY_PATH = Path("data/cuda/stage5b-cuda-parity-harness-summary.yaml")

STAGE5A_TARGET_PLAN_PATH = Path("data/cuda/stage5a-cuda-target-plan.yaml")
STAGE5A_PARITY_SCAFFOLD_PATH = Path("data/cuda/stage5a-cuda-parity-scaffold.yaml")
STAGE5A_IMPLEMENTATION_GATES_PATH = Path("data/cuda/stage5a-cuda-implementation-gates.yaml")
STAGE5A_NON_TARGETS_PATH = Path("data/cuda/stage5a-cuda-non-targets.yaml")
STAGE5A_SUMMARY_PATH = Path("data/cuda/stage5a-cuda-planning-summary.yaml")
STAGE4Q_READINESS_PATH = Path("data/benchmarks/stage4q-cuda-parity-readiness.yaml")
STAGE4Q_SUMMARY_PATH = Path("data/research/stage4q-cpu-benchmark-parity-planning-summary.yaml")
STAGE4O_SUMMARY_PATH = Path("data/research/stage4o-cpu-batch-adapter-expansion-summary.yaml")
STAGE4P_SUMMARY_PATH = Path("data/research/stage4p-result-store-score-summary-unification-summary.yaml")

HARNESS_SCHEMA = Path("schemas/cuda/cuda-parity-harness-record-v0.schema.json")
FIXTURE_SCHEMA = Path("schemas/cuda/cuda-parity-fixture-record-v0.schema.json")
BACKEND_SCHEMA = Path("schemas/cuda/cuda-backend-capability-record-v0.schema.json")
MATRIX_SCHEMA = Path("schemas/cuda/cuda-future-kernel-parity-matrix-v0.schema.json")
SUMMARY_SCHEMA = Path("schemas/cuda/stage5b-cuda-parity-harness-summary-v0.schema.json")

HARNESS_REPORT = "harness_plan_report.json"
FIXTURE_REPORT = "parity_fixtures_report.json"
BACKEND_REPORT = "backend_capability_report.json"
MATRIX_REPORT = "future_kernel_parity_matrix_report.json"
SUMMARY_REPORT = "summary.json"
WARNINGS_JSONL = "warnings.jsonl"

CUDA_PARITY_POLICY = {
    "cuda_parity_harness_only": True,
    "cuda_implementation_added": False,
    "cuda_kernel_added": False,
    "cuda_source_modified": False,
    "gpu_benchmark_performed": False,
    "performance_claim": False,
    "speedup_claim": False,
    "broad_experiment_executed": False,
    "raw_data_processed": False,
    "solve_claim": False,
    "no_solve_claim": True,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "generated_outputs_committed": False,
    "codex_output_committed": False,
    "website_expansion": False,
    "cuda_used": False,
    "cuda_required": False,
}

FUTURE_KERNEL_DEFINITIONS = (
    ("shift_score_kernel", "caesar_mod29", "planned"),
    ("affine_score_kernel", "affine_mod29", "planned"),
    ("vigenere_score_kernel", "vigenere", "planned"),
    ("prime_minus_one_stream_score_kernel", "prime_minus_one_stream", "planned"),
    ("prime_gap_stream_score_kernel", "prime_gap_stream", "blocked"),
    ("crib_match_kernel", "scoring_crib_checks", "planned"),
    ("ngram_score_kernel", "scoring_ngram_proxy", "planned"),
    ("topk_reduce_kernel", "topk_result_ordering", "planned"),
    ("batch_transform_dispatch_kernel", "cpu_batch_dispatch", "planned"),
)

BAD_TRUE_FLAGS = (
    "cuda_implementation_added",
    "cuda_kernel_added",
    "cuda_source_modified",
    "gpu_benchmark_performed",
    "performance_claim",
    "speedup_claim",
    "broad_experiment_executed",
    "raw_data_processed",
    "solve_claim",
    "canonical_corpus_active",
    "page_boundaries_final",
    "generated_outputs_committed",
    "codex_output_committed",
    "website_expansion",
)
