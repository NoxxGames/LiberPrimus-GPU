"""Shared constants for Stage 4C visual annotation."""

from __future__ import annotations

from pathlib import Path

DEFAULT_VISUAL_OBSERVATIONS = Path(
    "data/observations/visual/stage4b-visual-observation-records.yaml"
)
DEFAULT_NEGATIVE_CONTROLS = Path("data/observations/research/stage4b-negative-control-records.yaml")
DEFAULT_IMAGE_ARTIFACTS = Path("data/observations/visual/liber-primus-page-image-artifacts-v0.jsonl")
DEFAULT_IMAGE_LOCKS = Path(
    "data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl"
)
DEFAULT_IMAGE_DIR = Path("third_party/LiberPrimusPages")
DEFAULT_OUTPUT_DIR = Path("experiments/results/visual-annotation/stage4c")
DEFAULT_TASKS = Path("data/observations/visual/stage4c-visual-annotation-tasks.yaml")
DEFAULT_CUNEIFORM = Path("data/observations/visual/stage4c-cuneiform-reading-candidates.yaml")
DEFAULT_DOT = Path("data/observations/visual/stage4c-dot-pattern-annotation-tasks.yaml")
DEFAULT_DELIMITER = Path("data/observations/visual/stage4c-delimiter-annotation-tasks.yaml")
DEFAULT_NEGATIVE = Path(
    "data/observations/visual/stage4c-visual-negative-control-annotation-tasks.yaml"
)
DEFAULT_SUMMARY = Path("data/observations/visual/stage4c-annotation-pack-summary.yaml")

ANNOTATION_STATUSES = {
    "pending",
    "needs_human_coordinates",
    "human_review_required",
    "annotated",
    "rejected",
    "superseded",
}
COORDINATE_SYSTEMS = {"pixel_absolute", "normalized_0_1", "unknown_pending_annotation"}

VISUAL_NEGATIVE_CONTROL_CLASSES = {
    "braille_dot_readings",
    "constellation_dot_readings",
    "forced_13_31_dot_values",
    "cuneiform_reading_as_fact",
    "incorrect_base60_conversion",
    "ad_hoc_prime_magic_square_arithmetic",
    "spectrogram_pareidolia",
    "ai_generated_page_solves",
    "geometry_mirror_overlay_dumps",
    "mayfly_dot_skip_index_theory",
}

SCHEMA_PATHS = {
    "tasks": Path("schemas/visual/visual-annotation-task-v0.schema.json"),
    "cuneiform": Path("schemas/visual/cuneiform-reading-candidate-v0.schema.json"),
    "dot": Path("schemas/visual/dot-pattern-annotation-v0.schema.json"),
    "delimiter": Path("schemas/visual/delimiter-annotation-v0.schema.json"),
    "negative": Path("schemas/visual/visual-negative-control-annotation-v0.schema.json"),
    "summary": Path("schemas/visual/visual-annotation-pack-summary-v0.schema.json"),
}
