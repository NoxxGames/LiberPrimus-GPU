"""Summaries for Stage 4N stego/audio positive-control readiness."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.stego_positive_controls.models import BLOCKED_READY_STATES, COMMON_FALSE_FLAGS


def summarize_positive_controls(
    *,
    outguess_readiness: list[dict[str, Any]],
    audio_readiness: list[dict[str, Any]],
    fixture_cache: list[dict[str, Any]],
    expected_outputs: list[dict[str, Any]],
    toolchain: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build the committed singleton Stage 4N summary."""

    all_readiness = outguess_readiness + audio_readiness
    historical = [record for record in all_readiness if not record.get("synthetic") and record.get("ready_state") != "reference_only"]
    ready_count = sum(record.get("ready_state") == "ready_with_cached_asset_and_expected_output" for record in historical)
    blocked_count = sum(record.get("ready_state") in BLOCKED_READY_STATES for record in historical)
    synthetic_ready = sum(record.get("ready_state") == "synthetic_ready" for record in all_readiness)
    state_counts: dict[str, int] = {}
    for record in all_readiness:
        state = str(record.get("ready_state"))
        state_counts[state] = state_counts.get(state, 0) + 1
    toolchain_summary = {str(record.get("toolchain")): str(record.get("toolchain_state")) for record in toolchain}
    return {
        "record_type": "stego_positive_control_summary",
        "stage": "stage4n",
        "outguess_readiness_records_count": len(outguess_readiness),
        "audio_readiness_records_count": len(audio_readiness),
        "fixture_cache_records_count": len(fixture_cache),
        "expected_output_records_count": len(expected_outputs),
        "toolchain_readiness_records_count": len(toolchain),
        "historical_fixtures_ready_count": ready_count,
        "historical_fixtures_blocked_count": blocked_count,
        "synthetic_controls_ready_count": synthetic_ready,
        "ready_state_counts": state_counts,
        "toolchain_availability_summary": toolchain_summary,
        "generated_outputs_committed": False,
        "raw_cache_staged": False,
        **COMMON_FALSE_FLAGS,
    }


def load_summary(path: Path) -> dict[str, Any]:
    """Load a committed Stage 4N summary."""

    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
