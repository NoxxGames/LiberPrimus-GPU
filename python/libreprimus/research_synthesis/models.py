"""Models and constants for Stage 3Y research-synthesis records."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

DEFAULT_DATA_DIR = Path("data/research")
DEFAULT_STAGED_PLAN = Path("docs/roadmap/staged-plan.md")

ALLOWED_METHOD_STATUSES = {
    "active",
    "promising",
    "inconclusive",
    "noisy",
    "negative",
    "retired",
    "deferred",
    "infrastructure_only",
}

ALLOWED_RETIREMENT_STATUSES = {
    "retired",
    "deprioritised",
    "deferred",
    "active_with_constraints",
}

REQUIRED_METHOD_FAMILIES = {
    "caesar_affine",
    "reverse_reranked_affine",
    "vigenere_tiny_motif",
    "vigenere_lp_evidence_pack",
    "vigenere_historical_motif_pack",
    "p56_local_prime_offsets",
    "reset_advance_ablation",
    "mersenne_perfect_number_probe",
    "onion7_explicit_seed_pack",
    "cookie_hash_sha256_packs",
    "gp_rune_claim_verifier",
    "observation_review_workflow",
    "observation_promotion_ledger",
    "image_source_variant_compression_preflight",
    "stego_audio_positive_control_readiness",
    "source_lock_snapshots",
    "scoring_consolidation",
    "result_store_score_summary_unification",
    "cpu_benchmark_parity_planning",
    "cuda_planning_parity_scaffolding",
    "cuda_parity_harness_skeleton",
    "cuda_build_device_detection",
    "native_cpp_cpu_backend",
    "cuda_first_kernel_contract",
    "cuda_synthetic_shift_kernel",
    "deterministic_image_analysis",
    "image_transform_suite",
    "discord_ingestion_review",
    "discord_lead_promotion",
    "outguess_regression_harness",
    "cuda_gpu_acceleration",
}


@dataclass(frozen=True)
class RecordSetSpec:
    key: str
    filename: str
    schema_path: Path
    record_type: str


RECORD_SET_SPECS = (
    RecordSetSpec(
        "stage_summaries",
        "stage-summary-records-v0.yaml",
        Path("schemas/research/stage-summary-record-v0.schema.json"),
        "stage_summary_record",
    ),
    RecordSetSpec(
        "method_families",
        "method-family-status-records-v0.yaml",
        Path("schemas/research/method-family-status-record-v0.schema.json"),
        "method_family_status_record",
    ),
    RecordSetSpec(
        "method_retirements",
        "method-retirement-records-v0.yaml",
        Path("schemas/research/method-retirement-record-v0.schema.json"),
        "method_retirement_record",
    ),
    RecordSetSpec(
        "deep_research_influences",
        "deep-research-influence-records-v0.yaml",
        Path("schemas/research/deep-research-influence-record-v0.schema.json"),
        "deep_research_influence_record",
    ),
    RecordSetSpec(
        "direction_changes",
        "project-direction-change-records-v0.yaml",
        Path("schemas/research/project-direction-change-record-v0.schema.json"),
        "project_direction_change_record",
    ),
)
