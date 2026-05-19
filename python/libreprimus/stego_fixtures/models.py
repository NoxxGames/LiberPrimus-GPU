"""Constants for Stage 4F stego fixture source-locking."""

from __future__ import annotations

from pathlib import Path


DEFAULT_OUTPUT_DIR = Path("experiments/results/stego-fixtures/stage4f")
DEFAULT_STAGE4E_SOURCE_DELTA = Path("data/observations/archive/stage4e-cicada-solvers-iddqd-source-delta.yaml")
DEFAULT_STAGE4E_SOURCE_HEALTH = Path("data/locks/third-party/stage4e-cicada-solvers-iddqd-source-health.yaml")
DEFAULT_STAGE4B_SOURCES = Path("data/observations/archive/stage4b-promoted-source-records.yaml")
DEFAULT_OUTGUESS_FIXTURES = Path("data/observations/stego/stage4f-outguess-fixture-source-records.yaml")
DEFAULT_AUDIO_FIXTURES = Path("data/observations/stego/stage4f-audio-fixture-source-records.yaml")
DEFAULT_SOURCE_HEALTH = Path("data/locks/third-party/stage4f-stego-fixture-source-health.yaml")
DEFAULT_TOOLCHAIN = Path("data/observations/stego/stage4f-toolchain-requirements.yaml")
DEFAULT_MANIFEST_DIR = Path("experiments/manifests/stego/stage4f-disabled")

DISABLED_MANIFEST_IDS = {
    "exp_stage4f_outguess_positive_negative_matrix",
    "exp_stage4f_openpuff_interconnectedness_fixture_prep",
    "exp_stage4f_mp3_instar_regression_prep",
    "exp_stage4f_audio_hexdump_string_baseline",
}

IDDDQ_REPO_BLOB_BASE = "https://github.com/cicada-solvers/iddqd/blob/master"
IDDDQ_REPO_TREE_BASE = "https://github.com/cicada-solvers/iddqd/tree/master"
