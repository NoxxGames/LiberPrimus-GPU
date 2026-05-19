"""Constants and shared flags for Stage 4N stego/audio readiness."""

from __future__ import annotations

from pathlib import Path

DEFAULT_OUTGUESS_SOURCES = Path("data/observations/stego/stage4f-outguess-fixture-source-records.yaml")
DEFAULT_AUDIO_SOURCES = Path("data/observations/stego/stage4f-audio-fixture-source-records.yaml")
DEFAULT_SOURCE_HEALTH = Path("data/locks/third-party/stage4f-stego-fixture-source-health.yaml")
DEFAULT_TOOLCHAIN_REQUIREMENTS = Path("data/observations/stego/stage4f-toolchain-requirements.yaml")
DEFAULT_SOURCE_LOCKS = Path("data/locks/third-party/source-snapshots/stage4k-source-lock-snapshot-records.yaml")
DEFAULT_SOURCE_FETCHES = Path("data/locks/third-party/source-snapshots/stage4k-source-fetch-records.yaml")
DEFAULT_SOURCE_LOCK_SUMMARY = Path("data/locks/third-party/source-snapshots/stage4k-source-lock-summary.yaml")
DEFAULT_OUTGUESS_ARTIFACTS = Path("data/observations/stego/outguess-artifacts-v0.yaml")
DEFAULT_MANIFEST_READINESS = Path("data/observations/review/stage4l-manifest-readiness-records.yaml")
DEFAULT_CACHE_DIR = Path("third_party/StegoPositiveControls")
DEFAULT_OUT_DIR = Path("experiments/results/stego-positive-controls/stage4n")
DEFAULT_OUTGUESS_READINESS_OUT = Path("data/observations/stego/stage4n-outguess-positive-control-readiness.yaml")
DEFAULT_AUDIO_READINESS_OUT = Path("data/observations/stego/stage4n-audio-positive-control-readiness.yaml")
DEFAULT_FIXTURE_CACHE_OUT = Path("data/observations/stego/stage4n-fixture-cache-records.yaml")
DEFAULT_EXPECTED_OUTPUT_OUT = Path("data/observations/stego/stage4n-expected-output-records.yaml")
DEFAULT_TOOLCHAIN_OUT = Path("data/observations/stego/stage4n-toolchain-readiness.yaml")
DEFAULT_SUMMARY_OUT = Path("data/observations/stego/stage4n-positive-control-summary.yaml")

COMMON_FALSE_FLAGS: dict[str, bool] = {
    "raw_file_committed": False,
    "binary_committed": False,
    "image_committed": False,
    "audio_committed": False,
    "font_committed": False,
    "archive_committed": False,
    "extracted_payload_committed": False,
    "solve_claim": False,
    "execution_performed": False,
    "tool_executed": False,
}

REAL_EXECUTION_READY_STATES = {"ready_with_cached_asset_and_expected_output"}
BLOCKED_READY_STATES = {
    "cached_asset_missing_expected_output",
    "source_only_missing_asset",
    "source_only_missing_expected_output",
    "blocked_tool_unavailable",
    "blocked_expected_output_unknown",
    "blocked_asset_not_cached",
    "blocked_manual_source_review",
}
