"""Validation for Stage 4E source-delta records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.source_delta_audit.models import DISABLED_MANIFEST_IDS


def load_yaml_records(path: Path) -> list[dict[str, Any]]:
    """Load records from a Stage-style YAML record set or a single YAML dict."""

    if not path.is_file():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if isinstance(data, dict) and isinstance(data.get("records"), list):
        return [record for record in data["records"] if isinstance(record, dict)]
    if isinstance(data, dict):
        return [data]
    return []


def write_yaml_records(path: Path, *, record_set_id: str, schema: str, records: list[dict[str, Any]]) -> None:
    """Write a Stage-style YAML record set."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(
            {"record_set_id": record_set_id, "schema": schema, "records": records},
            sort_keys=False,
            allow_unicode=False,
        ),
        encoding="utf-8",
    )


def validate_source_delta_records(
    *,
    source_delta: Path,
    source_health: Path,
    image_artifact: Path,
    manifest_dir: Path,
) -> tuple[dict[str, int], list[str]]:
    """Validate committed Stage 4E source-delta records."""

    errors: list[str] = []
    delta_records = load_yaml_records(source_delta)
    health_records = load_yaml_records(source_health)
    artifact_records = load_yaml_records(image_artifact)
    manifest_paths = sorted(manifest_dir.glob("exp_stage4e_*.yaml")) if manifest_dir.is_dir() else []
    counts = {
        "source_delta_records": len(delta_records),
        "source_health_records": len(health_records),
        "image_artifact_records": len(artifact_records),
        "disabled_manifests": len(manifest_paths),
    }
    if not delta_records:
        errors.append("source_delta_records_missing")
    if not health_records:
        errors.append("source_health_records_missing")
    if not artifact_records:
        errors.append("image_artifact_records_missing")
    for record in [*delta_records, *health_records, *artifact_records]:
        _validate_common_flags(record, errors)
    for record in artifact_records:
        if record.get("usable_as_experiment_seed") is not False:
            errors.append(f"image_artifact_seed_not_false:{record.get('observation_id')}")
        if not record.get("future_tests") or not record.get("negative_controls"):
            errors.append(f"image_artifact_missing_tests_or_controls:{record.get('observation_id')}")
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
    label = str(record.get("audit_id") or record.get("source_id") or record.get("observation_id") or record.get("manifest_id") or record.get("record_type"))
    for key in ("raw_file_committed", "binary_committed", "font_committed"):
        if key in record and record.get(key) is not False:
            errors.append(f"{key}_not_false:{label}")
    if record.get("solve_claim") is not False:
        errors.append(f"solve_claim_not_false:{label}")
    if record.get("trusted_as_canonical") is True:
        errors.append(f"trusted_as_canonical_true:{label}")
