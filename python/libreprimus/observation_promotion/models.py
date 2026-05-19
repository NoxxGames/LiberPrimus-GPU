"""Models and constants for Stage 4L observation promotion."""

from __future__ import annotations

from pathlib import Path

DEFAULT_OUT_DIR = Path("experiments/results/observation-promotion/stage4l")
DEFAULT_LEDGER_OUT = Path(
    "data/observations/review/stage4l-reviewed-observation-promotion-ledger.yaml"
)
DEFAULT_READINESS_OUT = Path(
    "data/observations/review/stage4l-observation-promotion-readiness-records.yaml"
)
DEFAULT_BLOCKERS_OUT = Path(
    "data/observations/review/stage4l-observation-promotion-blocker-records.yaml"
)
DEFAULT_MANIFEST_READINESS_OUT = Path(
    "data/observations/review/stage4l-manifest-readiness-records.yaml"
)
DEFAULT_SUMMARY_OUT = Path(
    "data/observations/review/stage4l-reviewed-observation-promotion-summary.yaml"
)

STAGE4J_DECISIONS = Path("data/observations/review/stage4j-observation-review-decisions.yaml")
STAGE4J_PROMOTIONS = Path("data/observations/review/stage4j-observation-promotion-records.yaml")
STAGE4J_QUARANTINE = Path("data/observations/review/stage4j-observation-quarantine-records.yaml")
STAGE4J_SUMMARY = Path("data/observations/review/stage4j-observation-review-summary.yaml")
STAGE4K_SNAPSHOT_RECORDS = Path(
    "data/locks/third-party/source-snapshots/stage4k-source-lock-snapshot-records.yaml"
)
STAGE4K_FETCH_RECORDS = Path(
    "data/locks/third-party/source-snapshots/stage4k-source-fetch-records.yaml"
)
STAGE4K_SUMMARY = Path("data/locks/third-party/source-snapshots/stage4k-source-lock-summary.yaml")
STAGE4G_COOKIE_SUMMARY = Path("data/observations/web/stage4g-cookie-refresh-summary.yaml")
STAGE4L_COMMUNITY_INTAKE = Path("data/observations/review/stage4l-community-observation-intake.yaml")

RELEVANT_RECORD_PATHS = (
    Path("data/observations/visual/stage4b-visual-observation-records.yaml"),
    Path("data/observations/visual/stage4c-visual-annotation-tasks.yaml"),
    Path("data/observations/visual/stage4c-cuneiform-reading-candidates.yaml"),
    Path("data/observations/visual/stage4c-dot-pattern-annotation-tasks.yaml"),
    Path("data/observations/visual/stage4c-delimiter-annotation-tasks.yaml"),
    Path("data/observations/visual/stage4c-visual-negative-control-annotation-tasks.yaml"),
    Path("data/observations/research/stage4b-negative-control-records.yaml"),
    STAGE4G_COOKIE_SUMMARY,
    Path("data/observations/stego/stage4f-outguess-fixture-source-records.yaml"),
    Path("data/observations/stego/stage4f-audio-fixture-source-records.yaml"),
    STAGE4L_COMMUNITY_INTAKE,
)

DISABLED_MANIFEST_DIRS = (
    Path("experiments/manifests/stage4b-disabled"),
    Path("experiments/manifests/stego/stage4f-disabled"),
    Path("experiments/manifests/stage4e-disabled"),
)

PROMOTION_CATEGORIES = (
    "ready_for_manifest",
    "ready_as_control_only",
    "source_reference_only",
    "blocked_needs_coordinates",
    "blocked_needs_source_lock",
    "blocked_needs_human_review",
    "blocked_ambiguous_reading",
    "blocked_missing_expected_output",
    "blocked_toolchain_unavailable",
    "blocked_negative_result",
    "quarantined_false_positive",
    "rejected",
    "deferred",
)

LOCKED_SOURCE_STATUSES = {
    "source_locked",
    "metadata_locked",
    "snapshot_cached_ignored",
    "commit_address_locked",
}

FUTURE_MANIFEST_TARGETS = (
    "gp_rune_verifier_batch002",
    "dot_ambiguity_audit_v1",
    "delimiter_handedness_v1",
    "onion7_raw_routes_v1",
    "cookie_pack_v2",
    "cuneiform_reading_pack_v1",
    "visual_negative_controls_v1",
    "outguess_positive_negative_matrix",
    "mp3_instar_regression_prep",
    "lp_image_variant_hash_dimension_audit",
    "image_compression_artifact_preflight",
    "cpu_batch_expansion_future",
    "exp_stage4m_bigram_diagonal_fibonacci_421_audit",
)


def safety_flags() -> dict[str, bool]:
    """Return Stage 4L no-execution/no-solve flags."""

    return {
        "execution_enabled": False,
        "solve_claim": False,
        "trusted_as_canonical": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "cuda_used": False,
        "generated_outputs_committed": False,
        "raw_data_processed": False,
    }
