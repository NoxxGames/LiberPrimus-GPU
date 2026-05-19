"""Constants for Stage 4E source-delta audit."""

from __future__ import annotations

from pathlib import Path

DEFAULT_REPO_URL = "https://github.com/cicada-solvers/iddqd.git"
DEFAULT_CACHE_DIR = Path("third_party/CicadaSolversIddqd")
DEFAULT_OUTPUT_DIR = Path("experiments/results/source-delta/stage4e")
DEFAULT_SOURCE_DELTA = Path("data/observations/archive/stage4e-cicada-solvers-iddqd-source-delta.yaml")
DEFAULT_SOURCE_HEALTH = Path("data/locks/third-party/stage4e-cicada-solvers-iddqd-source-health.yaml")
DEFAULT_IMAGE_ARTIFACT = Path("data/observations/visual/stage4e-image-compression-artifact-observations.yaml")
DEFAULT_MANIFEST_DIR = Path("experiments/manifests/stage4e-disabled")

SOURCE_ID = "stage4e-cicada-solvers-iddqd"

SELECTED_CATEGORY_ORDER = (
    "lp_full_image",
    "lp_unsolved_image",
    "lp_outguessed",
    "historical_2012",
    "historical_2013",
    "historical_2014",
    "historical_2016",
    "audio_fixture_candidate",
    "image_fixture_candidate",
    "transcription",
    "translation",
    "key",
    "byte_string",
    "tooling",
    "font_metadata_only",
)

DISABLED_MANIFEST_IDS = (
    "exp_stage4e_lp_image_variant_hash_dimension_audit",
    "exp_stage4e_image_compression_artifact_preflight",
    "exp_stage4e_lp_outguessed_fixture_source_lock",
    "exp_stage4e_audio_fixture_source_lock",
)
