"""Models and constants for Stage 4Q benchmark planning."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-4q"
STAGE4Q_OUTPUT_DIR = Path("experiments/results/benchmarks/stage4q")
STAGE4Q_PLAN_PATH = Path("data/benchmarks/stage4q-cpu-benchmark-plan.yaml")
STAGE4Q_READINESS_PATH = Path("data/benchmarks/stage4q-cuda-parity-readiness.yaml")
STAGE4Q_SUMMARY_PATH = Path("data/research/stage4q-cpu-benchmark-parity-planning-summary.yaml")

STAGE4O_SUMMARY_PATH = Path("data/research/stage4o-cpu-batch-adapter-expansion-summary.yaml")
STAGE4P_SUMMARY_PATH = Path("data/research/stage4p-result-store-score-summary-unification-summary.yaml")
STAGE4O_ADAPTER_COVERAGE_PATH = Path("experiments/results/cpu-batch/stage4o/adapter_coverage.json")
STAGE4O_PARITY_EXPECTATIONS_PATH = Path("experiments/results/cpu-batch/stage4o/parity_expectations.jsonl")
STAGE4O_RESULT_RECORDS_PATH = Path("experiments/results/cpu-batch/stage4o/result_records.jsonl")

PLAN_SCHEMA = Path("schemas/benchmarks/cpu-benchmark-plan-v0.schema.json")
SMOKE_SCHEMA = Path("schemas/benchmarks/cpu-benchmark-smoke-record-v0.schema.json")
ENVIRONMENT_SCHEMA = Path("schemas/benchmarks/benchmark-environment-record-v0.schema.json")
READINESS_SCHEMA = Path("schemas/benchmarks/cuda-parity-benchmark-readiness-v0.schema.json")
SUMMARY_SCHEMA = Path("schemas/benchmarks/stage4q-benchmark-parity-summary-v0.schema.json")

ENVIRONMENT_JSON = "benchmark_environment.json"
SMOKE_JSONL = "cpu_benchmark_smoke_records.jsonl"
READINESS_JSON = "cuda_parity_readiness.json"
SUMMARY_JSON = "summary.json"
WARNINGS_JSONL = "warnings.jsonl"

CPU_ONLY_POLICY = {
    "cpu_only": True,
    "cuda_used": False,
    "cuda_required": False,
    "gpu_benchmark_performed": False,
    "cuda_implementation_added": False,
    "no_solve_claim": True,
    "solve_claim": False,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "generated_outputs_committed": False,
    "raw_data_processed": False,
    "broad_experiment_executed": False,
}

BENCHMARK_PLAN_TIERS = (
    {
        "plan_id": "stage4q-tier0-environment-record",
        "benchmark_scope": "environment_record",
        "benchmark_status": "planned",
        "tier": "tier0_environment",
        "description": "Record raw-data-free local CPU/Python/Git context before any future benchmark comparison.",
    },
    {
        "plan_id": "stage4q-tier1-cpu-smoke",
        "benchmark_scope": "cpu_smoke",
        "benchmark_status": "smoke_passed",
        "tier": "tier1_cpu_smoke",
        "description": "Run a tiny deterministic CPU-only diagnostic to prove hashing and summary plumbing.",
    },
    {
        "plan_id": "stage4q-tier2-solved-fixture-parity",
        "benchmark_scope": "planning_only",
        "benchmark_status": "planned",
        "tier": "tier2_solved_fixture_parity",
        "description": "Reuse Stage 4O solved-fixture-safe streams for future benchmark comparisons.",
    },
    {
        "plan_id": "stage4q-tier3-transform-score-shape",
        "benchmark_scope": "planning_only",
        "benchmark_status": "planned",
        "tier": "tier3_transform_score_shape",
        "description": "Require Stage 4I score-summary shape and Stage 4P result-surface compatibility.",
    },
    {
        "plan_id": "stage4q-tier4-future-cuda-gates",
        "benchmark_scope": "parity_readiness",
        "benchmark_status": "planned",
        "tier": "tier4_future_cuda_gates",
        "description": "Document future CUDA parity gates without implementing CUDA or running GPU benchmarks.",
    },
)

FALLBACK_ADAPTER_COVERAGE = (
    ("direct_translation", "direct_translation", "supported"),
    ("reverse_gematria", "reverse_gematria", "supported"),
    ("rotated_reverse_gematria", "rotated_reverse_gematria", "supported"),
    ("vigenere_explicit_key", "vigenere_explicit_key", "supported"),
    ("prime_minus_one_stream", "prime_minus_one_stream", "supported"),
    ("phi_prime_stream", "phi_prime_stream", "supported"),
    ("caesar_shift", "caesar_mod29", "supported"),
    ("affine_mod29", "affine_mod29", "supported"),
    ("p56_prime_minus_one", "p56_prime_minus_one", "supported"),
    ("reset_advance_variants", "reset_advance", "deferred"),
    ("historical_motif_vigenere", "historical_motif_vigenere", "deferred"),
    ("cookie_hash_family", "cookie_hash", "unsupported_by_design"),
    ("stego_audio_family", "stego_audio", "unsupported_by_design"),
    ("image_compression_bigram_family", "image_compression_bigram", "unsupported_by_design"),
)
