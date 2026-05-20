"""Models and constants for Stage 5A CUDA planning."""

from __future__ import annotations

from pathlib import Path

STAGE_ID = "stage-5a"

STAGE5A_OUTPUT_DIR = Path("experiments/results/cuda-planning/stage5a")
TARGET_PLAN_PATH = Path("data/cuda/stage5a-cuda-target-plan.yaml")
PARITY_SCAFFOLD_PATH = Path("data/cuda/stage5a-cuda-parity-scaffold.yaml")
IMPLEMENTATION_GATES_PATH = Path("data/cuda/stage5a-cuda-implementation-gates.yaml")
NON_TARGETS_PATH = Path("data/cuda/stage5a-cuda-non-targets.yaml")
SUMMARY_PATH = Path("data/cuda/stage5a-cuda-planning-summary.yaml")

STAGE4Q_READINESS_PATH = Path("data/benchmarks/stage4q-cuda-parity-readiness.yaml")
STAGE4Q_SUMMARY_PATH = Path("data/research/stage4q-cpu-benchmark-parity-planning-summary.yaml")
STAGE4O_SUMMARY_PATH = Path("data/research/stage4o-cpu-batch-adapter-expansion-summary.yaml")
STAGE4P_SUMMARY_PATH = Path("data/research/stage4p-result-store-score-summary-unification-summary.yaml")
STAGE4O_PARITY_EXPECTATIONS_PATH = Path("experiments/results/cpu-batch/stage4o/parity_expectations.jsonl")
STAGE4P_UNIFIED_RESULTS_PATH = Path("experiments/results/result-store-unification/stage4p/unified_result_records.jsonl")

TARGET_PLAN_SCHEMA = Path("schemas/cuda/cuda-target-plan-record-v0.schema.json")
PARITY_SCAFFOLD_SCHEMA = Path("schemas/cuda/cuda-parity-scaffold-record-v0.schema.json")
IMPLEMENTATION_GATE_SCHEMA = Path("schemas/cuda/cuda-implementation-gate-record-v0.schema.json")
NON_TARGET_SCHEMA = Path("schemas/cuda/cuda-non-target-record-v0.schema.json")
SUMMARY_SCHEMA = Path("schemas/cuda/cuda-planning-summary-v0.schema.json")

TARGET_PLAN_REPORT = "target_plan_report.json"
PARITY_SCAFFOLD_REPORT = "parity_scaffold_report.json"
IMPLEMENTATION_GATES_REPORT = "implementation_gates_report.json"
NON_TARGETS_REPORT = "non_targets_report.json"
SUMMARY_REPORT = "summary.json"
WARNINGS_JSONL = "warnings.jsonl"

CUDA_PLANNING_POLICY = {
    "cuda_planning_only": True,
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
    "cuda_used": False,
    "cuda_required": False,
}

NON_TARGET_DEFINITIONS = (
    (
        "discord_source_discovery_raw_logs",
        "Discord source discovery and raw logs",
        "Discord processing is source-review and privacy work, not a CUDA transform target.",
    ),
    (
        "image_interpretation_ocr_ai_ml",
        "Image interpretation/OCR/AI/ML",
        "Visual interpretation is review-only and cannot become CUDA work without reviewed source and coordinate controls.",
    ),
    (
        "image_compression_star_artefacts",
        "Image compression and star-like artefacts",
        "Compression metrics are preflight observations, not CPU batch transform semantics.",
    ),
    (
        "bigram_fibonacci_421_observation",
        "Bigram/Fibonacci-421 observation",
        "The bigram claim is blocked pending reproducible matrix, rune order, and null controls.",
    ),
    (
        "stego_audio_extraction_tools",
        "OutGuess/OpenPuff/MP3Stego/audio extraction",
        "Stego/audio readiness requires fixtures and expected outputs; it is not a CUDA text-transform target.",
    ),
    (
        "cookie_hash_cracking_hashcat",
        "Cookie/hash cracking/hashcat",
        "Cookie/hash work is exact digest comparison and explicitly not transform adapter acceleration.",
    ),
    (
        "broad_unsolved_page_campaigns",
        "Broad unsolved-page campaigns",
        "Broad campaigns require approval and corpus locks; Stage 5A is planning-only.",
    ),
    (
        "website_expansion_knowledge_hub",
        "Website expansion / knowledge hub",
        "Website expansion is deferred to Stage 6 and is not CUDA scope.",
    ),
)

IMPLEMENTATION_GATE_DEFINITIONS = (
    (
        "cpu_batch_adapter_contract_stable",
        "satisfied",
        ["Stage 4H/4O CPU batch adapter records exist and preserve transform semantics."],
    ),
    (
        "stage4o_parity_expectations_available",
        "satisfied",
        ["Stage 4O parity expectation hashes are available for ready planning targets."],
    ),
    (
        "stage4p_unified_result_surface_available",
        "satisfied",
        ["Stage 4P unified result surfaces are available for cross-stage comparison."],
    ),
    (
        "stage4q_benchmark_parity_plan_available",
        "satisfied",
        ["Stage 4Q benchmark/parity plan and readiness records are available."],
    ),
    (
        "target_specific_parity_scaffold_exists",
        "satisfied",
        ["Stage 5A writes one scaffold record for each ready planning target."],
    ),
    (
        "generated_output_ignore_policy_exists",
        "satisfied",
        ["Generated CUDA planning reports are ignored and not committed."],
    ),
    (
        "raw_data_free_ci_gate_exists",
        "satisfied",
        ["CI validation remains raw-data-free and does not require CUDA."],
    ),
    (
        "cuda_optional_build_remains_optional",
        "satisfied",
        ["Existing CUDA scaffold remains optional and is not required by CI."],
    ),
    (
        "no_speedup_claim_before_parity",
        "satisfied",
        ["No speedup claim may be made before exact CPU/GPU parity passes."],
    ),
    (
        "no_gpu_benchmark_before_parity",
        "satisfied",
        ["No GPU benchmark may run before parity harness and acceptance gates exist."],
    ),
)

FALLBACK_STAGE4O_PARITY_EXPECTATIONS = (
    (
        "stage4o-affine-local-v0",
        "affine_mod29",
        "6095c7c2871c79b9edf3026ea634b06b19c5bcaa833b4afaf77b3bd0c992cf0c",
        "7ba6044ebc98445670a40ce8c229d2b2ab4226ec65c78fa76e39ec56c25006eb",
    ),
    (
        "stage4o-caesar-local-v0",
        "caesar_mod29",
        "18f6990554d445d1bcae30cac2623872cf1cb2777958fe3fc9bc52e2965106d4",
        "5f748fedc4b16723551be7e209b41c57b75ee05a71f5984d7c1b399eb6ad435e",
    ),
    (
        "stage4o-direct-an-v0",
        "direct_translation",
        "5ac4d5d4c2d31e896d7d75569c3386ac6154b70a494fa618a8975974269ef290",
        "a53b79bd31b1401bc60a8b1bf33d105d358a56ba317886786ebcb5f09e5d7dd3",
    ),
    (
        "stage4o-phi-prime-an-v0",
        "phi_prime_stream",
        "5ac4d5d4c2d31e896d7d75569c3386ac6154b70a494fa618a8975974269ef290",
        "7064eeee7dfdad7d90c325c3cc8edf535f95b58f7965969a200736d52cacc2ff",
    ),
    (
        "stage4o-prime-minus-one-an-v0",
        "prime_minus_one_stream",
        "5ac4d5d4c2d31e896d7d75569c3386ac6154b70a494fa618a8975974269ef290",
        "7064eeee7dfdad7d90c325c3cc8edf535f95b58f7965969a200736d52cacc2ff",
    ),
    (
        "stage4o-reverse-an-v0",
        "reverse_gematria",
        "5ac4d5d4c2d31e896d7d75569c3386ac6154b70a494fa618a8975974269ef290",
        "071d3466ac546037aaaa12ea9c340b4dc5de788cecf9988d3bfbf39c8a9d8370",
    ),
    (
        "stage4o-rotated-reverse-an-v0",
        "rotated_reverse_gematria",
        "5ac4d5d4c2d31e896d7d75569c3386ac6154b70a494fa618a8975974269ef290",
        "b9b1b40ec9f2dc729869ccfcc9435627ec2438e74ac9eef2b590f99f7a9d232f",
    ),
    (
        "stage4o-vigenere-an-v0",
        "vigenere_explicit_key",
        "5ac4d5d4c2d31e896d7d75569c3386ac6154b70a494fa618a8975974269ef290",
        "bafdaebce11fee8586a0965e917cab600406c6766fe26848beb6bddb8d4b0784",
    ),
)

FALLBACK_SCORE_SUMMARY_SHAPE_HASH = "91bd19dd38957dc0a18c6b05a8e8f4ff2ee9a799a1b6162e18098d575285fdf9"
FALLBACK_STAGE4P_UNIFIED_RESULT_ID = "stage4p-31e312cdaefa0ffa1326"
