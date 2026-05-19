"""Constants and light data models for Stage 4J observation review."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_OUT_DIR = Path("experiments/results/observation-review/stage4j")
DEFAULT_POLICY_OUT = Path("data/observations/review/stage4j-observation-review-policy.yaml")
DEFAULT_DECISIONS_OUT = Path("data/observations/review/stage4j-observation-review-decisions.yaml")
DEFAULT_PROMOTIONS_OUT = Path("data/observations/review/stage4j-observation-promotion-records.yaml")
DEFAULT_QUARANTINE_OUT = Path("data/observations/review/stage4j-observation-quarantine-records.yaml")
DEFAULT_SUMMARY_OUT = Path("data/observations/review/stage4j-observation-review-summary.yaml")

REVIEW_STATES = (
    "pending",
    "needs_human_review",
    "needs_source_lock",
    "needs_coordinates",
    "accepted",
    "rejected",
    "deferred",
    "quarantined",
    "superseded",
    "negative_control",
    "promoted_to_manifest",
)

OBSERVATION_TYPES = (
    "visual_cuneiform_candidate",
    "visual_dot_pattern_candidate",
    "delimiter_candidate",
    "numeric_claim",
    "gp_rune_claim",
    "source_link",
    "cookie_hash_candidate",
    "stego_audio_fixture_candidate",
    "image_compression_artifact_candidate",
    "discord_derived_lead",
    "negative_control",
)

PROMOTION_GATES = (
    "source_locked_or_synthetic_fixture",
    "review_state_accepted_or_promoted",
    "solve_claim_false",
    "trusted_as_canonical_false_by_default",
    "usable_as_experiment_seed_requires_explicit_promotion",
    "visual_requires_page_or_image_reference",
    "visual_seed_requires_coordinates_or_non_coordinate_rationale",
    "cuneiform_seed_requires_accepted_reading_and_coordinates",
    "dot_seed_requires_unambiguous_ordering_polarity_and_coordinates",
    "discord_seed_requires_public_source_corroboration",
    "negative_controls_only_promote_as_controls",
)

SOURCE_RECORD_PATHS = {
    "stage4b_visual": Path("data/observations/visual/stage4b-visual-observation-records.yaml"),
    "stage4c_tasks": Path("data/observations/visual/stage4c-visual-annotation-tasks.yaml"),
    "stage4c_cuneiform": Path("data/observations/visual/stage4c-cuneiform-reading-candidates.yaml"),
    "stage4c_dot": Path("data/observations/visual/stage4c-dot-pattern-annotation-tasks.yaml"),
    "stage4c_delimiter": Path("data/observations/visual/stage4c-delimiter-annotation-tasks.yaml"),
    "stage4c_negative": Path("data/observations/visual/stage4c-visual-negative-control-annotation-tasks.yaml"),
    "stage4b_negative": Path("data/observations/research/stage4b-negative-control-records.yaml"),
    "stage4b_sources": Path("data/observations/archive/stage4b-promoted-source-records.yaml"),
    "stage4b_cookie_sources": Path("data/observations/web/stage4b-cookie-candidate-source-records.yaml"),
    "stage4g_cookie_summary": Path("data/observations/web/stage4g-cookie-refresh-summary.yaml"),
    "stage4f_outguess": Path("data/observations/stego/stage4f-outguess-fixture-source-records.yaml"),
    "stage4f_audio": Path("data/observations/stego/stage4f-audio-fixture-source-records.yaml"),
    "stage4e_image_artifacts": Path("data/observations/visual/stage4e-image-compression-artifact-observations.yaml"),
    "stage3r_discord_observations": Path("data/observations/discord/stage3r-promoted-observation-records.yaml"),
}


@dataclass(frozen=True)
class ObservationInput:
    """Normalized input record from one committed observation family."""

    source_family: str
    source_path: str
    observation_id: str
    observation_type: str
    payload: dict[str, Any] = field(default_factory=dict)
