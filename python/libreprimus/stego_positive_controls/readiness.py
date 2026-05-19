"""Readiness record builders for Stage 4N fixtures."""

from __future__ import annotations

from typing import Any

from libreprimus.stego_positive_controls.models import COMMON_FALSE_FLAGS


def build_readiness_record(
    record: dict[str, Any],
    *,
    category: str,
    cache_record: dict[str, Any],
    expected_record: dict[str, Any],
    toolchain_records: list[dict[str, Any]],
    record_type: str,
) -> dict[str, Any]:
    """Build one outguess or audio readiness record."""

    source_record_id = str(record.get("fixture_id") or record.get("artifact_id") or "unknown")
    synthetic = category.startswith("synthetic_")
    toolchain_states = _toolchain_states(record.get("toolchain", []), toolchain_records)
    blockers: list[str] = []
    if synthetic:
        ready_state = "synthetic_ready"
    elif "reference_only" in category or category == "lp_outguessed_reference":
        ready_state = "reference_only"
    else:
        if cache_record.get("local_availability") != "present_ignored_cache":
            blockers.append("asset_not_cached")
        if expected_record.get("expected_output_status") == "unknown":
            blockers.append("expected_output_unknown")
        if any(state in {"outguess_missing", "openpuff_manual_required", "mp3stego_manual_required", "missing"} for state in toolchain_states):
            blockers.append("toolchain_not_ready")
        ready_state = _blocked_state(blockers, cache_record)
    return {
        "record_type": record_type,
        "readiness_id": f"stage4n-readiness-{source_record_id}",
        "source_record_id": source_record_id,
        "source_url": record.get("source_url"),
        "source_path": record.get("source_path") or record.get("local_path"),
        "source_lock_status": record.get("source_lock_status"),
        "source_lock_record_id": record.get("source_lock_record_id"),
        "canonical_url": record.get("canonical_url"),
        "fixture_category": category,
        "ready_state": ready_state,
        "blockers": blockers,
        "cache_record_id": cache_record["cache_record_id"],
        "expected_output_id": expected_record["expected_output_id"],
        "expected_output_required": expected_record["expected_output_required"],
        "expected_output_hash": expected_record.get("expected_payload_sha256") or expected_record.get("expected_payload_text_sha256"),
        "toolchain_states": toolchain_states,
        "synthetic": synthetic,
        "trusted_as_canonical": False,
        "notes": record.get("notes"),
        **COMMON_FALSE_FLAGS,
    }


def _toolchain_states(required_tools: Any, toolchain_records: list[dict[str, Any]]) -> list[str]:
    lookup = {str(record.get("toolchain")): str(record.get("toolchain_state")) for record in toolchain_records}
    states: list[str] = []
    for tool in required_tools if isinstance(required_tools, list) else []:
        tool_name = str(tool)
        if tool_name == "hexdump/strings":
            states.append(lookup.get("hexdump/strings", "missing"))
        elif tool_name == "audio_rendering":
            states.append(lookup.get("audio_rendering", "not_applicable"))
        else:
            states.append(lookup.get(tool_name, "missing"))
    return states or ["not_applicable"]


def _blocked_state(blockers: list[str], cache_record: dict[str, Any]) -> str:
    if "expected_output_unknown" in blockers:
        return "blocked_expected_output_unknown"
    if "asset_not_cached" in blockers:
        return "blocked_asset_not_cached"
    if "toolchain_not_ready" in blockers:
        return "blocked_tool_unavailable"
    if cache_record.get("local_availability") == "present_ignored_cache":
        return "ready_with_cached_asset_and_expected_output"
    return "blocked_manual_source_review"
