"""Validation helpers for Stage 4N stego/audio readiness records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.stego_positive_controls.loaders import load_yaml_records

FALSE_FIELDS = (
    "raw_file_committed",
    "binary_committed",
    "image_committed",
    "audio_committed",
    "font_committed",
    "archive_committed",
    "extracted_payload_committed",
    "solve_claim",
    "execution_performed",
    "tool_executed",
)


def validate_stego_positive_control_records(
    *,
    outguess_readiness: Path,
    audio_readiness: Path,
    fixture_cache: Path,
    expected_output: Path,
    toolchain: Path,
    summary: Path,
) -> tuple[dict[str, int], list[str]]:
    """Validate committed Stage 4N records without requiring raw assets."""

    groups = {
        "outguess_readiness_records": load_yaml_records(outguess_readiness),
        "audio_readiness_records": load_yaml_records(audio_readiness),
        "fixture_cache_records": load_yaml_records(fixture_cache),
        "expected_output_records": load_yaml_records(expected_output),
        "toolchain_readiness_records": load_yaml_records(toolchain),
        "summary_records": load_yaml_records(summary),
    }
    errors: list[str] = []
    for group_name, records in groups.items():
        if not records:
            errors.append(f"{group_name}_missing")
        for index, record in enumerate(records):
            _validate_false_fields(record, label=f"{group_name}[{index}]", errors=errors)
            if group_name in {"outguess_readiness_records", "audio_readiness_records"}:
                _validate_readiness(record, label=f"{group_name}[{index}]", errors=errors)
            if group_name == "fixture_cache_records":
                _validate_cache(record, label=f"{group_name}[{index}]", errors=errors)
            if group_name == "expected_output_records":
                _validate_expected(record, label=f"{group_name}[{index}]", errors=errors)
    return {key: len(value) for key, value in groups.items()}, errors


def _validate_false_fields(record: dict[str, Any], *, label: str, errors: list[str]) -> None:
    for field in FALSE_FIELDS:
        if record.get(field) is not False:
            errors.append(f"{label}:{field}_must_be_false")


def _validate_readiness(record: dict[str, Any], *, label: str, errors: list[str]) -> None:
    if not record.get("source_record_id"):
        errors.append(f"{label}:source_record_id_missing")
    if not record.get("ready_state"):
        errors.append(f"{label}:ready_state_missing")
    if record.get("ready_state") == "ready_with_cached_asset_and_expected_output":
        if not record.get("expected_output_hash"):
            errors.append(f"{label}:ready_without_expected_output_hash")
    if record.get("synthetic") and not str(record.get("fixture_category", "")).startswith("synthetic_"):
        errors.append(f"{label}:synthetic_category_missing")


def _validate_cache(record: dict[str, Any], *, label: str, errors: list[str]) -> None:
    if record.get("cache_policy") == "cached_ignored" and not record.get("sha256"):
        errors.append(f"{label}:cached_record_missing_sha256")
    if record.get("binary_committed") or record.get("image_committed") or record.get("audio_committed"):
        errors.append(f"{label}:raw_artifact_commit_forbidden")


def _validate_expected(record: dict[str, Any], *, label: str, errors: list[str]) -> None:
    if record.get("expected_output_status") == "unknown" and record.get("expected_payload_sha256"):
        errors.append(f"{label}:unknown_expected_output_has_hash")
