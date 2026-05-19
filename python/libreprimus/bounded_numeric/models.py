"""Shared constants for Stage 4D bounded numeric verification."""

from __future__ import annotations

from pathlib import Path

DEFAULT_MANIFEST_DIR = Path("experiments/manifests/stage4b-disabled")
DEFAULT_STAGE4B_VISUAL = Path("data/observations/visual/stage4b-visual-observation-records.yaml")
DEFAULT_STAGE4C_TASKS = Path("data/observations/visual/stage4c-visual-annotation-tasks.yaml")
DEFAULT_STAGE4C_CUNEIFORM = Path("data/observations/visual/stage4c-cuneiform-reading-candidates.yaml")
DEFAULT_STAGE4C_DOT = Path("data/observations/visual/stage4c-dot-pattern-annotation-tasks.yaml")
DEFAULT_STAGE4C_DELIMITER = Path("data/observations/visual/stage4c-delimiter-annotation-tasks.yaml")
DEFAULT_STAGE4C_NEGATIVE = Path("data/observations/visual/stage4c-visual-negative-control-annotation-tasks.yaml")
DEFAULT_OUTPUT_DIR = Path("experiments/results/bounded-numeric/stage4d")

MANIFEST_GP_RUNE = "exp_stage4b_gp_rune_verifier_batch002"
MANIFEST_DOT_AMBIGUITY = "exp_stage4b_dot_ambiguity_audit_v1"
MANIFEST_DELIMITER = "exp_stage4b_delimiter_handedness_v1"
MANIFEST_ONION7 = "exp_stage4b_onion7_raw_routes_v1"
MANIFEST_COOKIE = "exp_stage4b_cookie_pack_v2"
MANIFEST_CUNEIFORM = "exp_stage4b_cuneiform_reading_pack_v1"
MANIFEST_VISUAL_NEGATIVE = "exp_stage4b_visual_negative_controls_v1"

EXPECTED_MANIFEST_IDS = {
    MANIFEST_GP_RUNE,
    MANIFEST_DOT_AMBIGUITY,
    MANIFEST_DELIMITER,
    MANIFEST_ONION7,
    MANIFEST_COOKIE,
    MANIFEST_CUNEIFORM,
    MANIFEST_VISUAL_NEGATIVE,
}

AUDIT_MANIFEST_IDS = {
    MANIFEST_DOT_AMBIGUITY,
    MANIFEST_DELIMITER,
    MANIFEST_VISUAL_NEGATIVE,
}

SKIP_MANIFEST_IDS = {
    MANIFEST_GP_RUNE,
    MANIFEST_ONION7,
}

DEFER_MANIFEST_IDS = {
    MANIFEST_COOKIE,
    MANIFEST_CUNEIFORM,
}

FIXED_ROUTES = (
    "row_major",
    "column_major",
    "reverse_row_major",
    "reverse_column_major",
    "clockwise_spiral",
    "counterclockwise_spiral",
)

SCHEMA_PATHS = {
    "manifest": Path("schemas/experiments/bounded-numeric-manifest-v0.schema.json"),
    "result": Path("schemas/experiments/bounded-numeric-result-record-v0.schema.json"),
    "negative": Path("schemas/experiments/numeric-negative-control-result-v0.schema.json"),
    "delimiter": Path("schemas/experiments/delimiter-handedness-audit-record-v0.schema.json"),
}
