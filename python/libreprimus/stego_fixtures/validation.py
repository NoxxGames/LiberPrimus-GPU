"""Validation for Stage 4F stego fixture source-lock records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.stego_fixtures.loaders import load_yaml_records
from libreprimus.stego_fixtures.models import DISABLED_MANIFEST_IDS


def validate_stego_fixture_records(
    *,
    outguess_fixtures: Path,
    audio_fixtures: Path,
    source_health: Path,
    toolchain: Path,
    manifest_dir: Path,
) -> tuple[dict[str, int], list[str]]:
    """Validate committed Stage 4F fixture records."""

    errors: list[str] = []
    outguess = load_yaml_records(outguess_fixtures)
    audio = load_yaml_records(audio_fixtures)
    health = load_yaml_records(source_health)
    tools = load_yaml_records(toolchain)
    manifest_paths = sorted(manifest_dir.glob("exp_stage4f_*.yaml")) if manifest_dir.is_dir() else []
    counts = {
        "outguess_fixture_source_records": len(outguess),
        "audio_fixture_source_records": len(audio),
        "source_health_records": len(health),
        "toolchain_requirement_records": len(tools),
        "disabled_manifests": len(manifest_paths),
    }
    if not outguess:
        errors.append("outguess_fixture_records_missing")
    if not audio:
        errors.append("audio_fixture_records_missing")
    if not health:
        errors.append("source_health_records_missing")
    if not tools:
        errors.append("toolchain_requirement_records_missing")
    for record in [*outguess, *audio, *health, *tools]:
        _validate_common_flags(record, errors)
    _validate_toolchains(tools, errors)
    manifest_ids = {path.stem for path in manifest_paths}
    missing = set(DISABLED_MANIFEST_IDS) - manifest_ids
    if missing:
        errors.append(f"missing_disabled_manifests:{sorted(missing)}")
    for path in manifest_paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        _validate_common_flags(data, errors)
        if data.get("execution_enabled") is not False:
            errors.append(f"manifest_execution_enabled:{path.name}")
    return counts, errors


def _validate_common_flags(record: dict[str, Any], errors: list[str]) -> None:
    label = str(record.get("fixture_id") or record.get("source_id") or record.get("requirement_id") or record.get("manifest_id") or record.get("record_type"))
    for key in (
        "raw_file_committed",
        "binary_committed",
        "audio_committed",
        "image_committed",
        "extracted_payload_committed",
        "font_committed",
    ):
        if key in record and record.get(key) is not False:
            errors.append(f"{key}_not_false:{label}")
    if record.get("solve_claim") is not False:
        errors.append(f"solve_claim_not_false:{label}")
    if record.get("trusted_as_canonical") is True:
        errors.append(f"trusted_as_canonical_true:{label}")


def _validate_toolchains(records: list[dict[str, Any]], errors: list[str]) -> None:
    seen = {str(record.get("toolchain")) for record in records}
    required = {"outguess", "openpuff", "mp3stego", "hexdump/strings", "audio_rendering"}
    missing = required - seen
    if missing:
        errors.append(f"toolchain_requirements_missing:{sorted(missing)}")
    for record in records:
        if record.get("execution_status") != "not_executed_stage4f":
            errors.append(f"toolchain_executed:{record.get('requirement_id')}")
