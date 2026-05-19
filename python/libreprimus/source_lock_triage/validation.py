"""Validation for Stage 4B source-lock triage records."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import json

from jsonschema import ValidationError, validate

from libreprimus.paths import repo_root
from libreprimus.source_lock_triage.loaders import load_yaml_payload, load_yaml_records


SCHEMA_MAP = {
    "promoted_sources": repo_root() / "schemas/history/stage4b-source-triage-record-v0.schema.json",
    "source_health": repo_root() / "schemas/history/source-health-record-v0.schema.json",
    "visual_observations": repo_root()
    / "schemas/visual/stage4b-visual-observation-record-v0.schema.json",
    "negative_controls": repo_root() / "schemas/research/negative-control-record-v1.schema.json",
    "disabled_manifest": repo_root()
    / "schemas/experiments/stage4b-disabled-experiment-manifest-v0.schema.json",
}


def validate_stage4b_records(
    *,
    promoted_sources: Path,
    source_health: Path,
    visual_observations: Path,
    negative_controls: Path,
    cookie_source_records: Path,
    manifest_dir: Path,
) -> tuple[dict[str, int], list[str]]:
    """Validate all committed Stage 4B records."""

    errors: list[str] = []
    counts: dict[str, int] = {}
    for key, path in (
        ("promoted_sources", promoted_sources),
        ("source_health", source_health),
        ("visual_observations", visual_observations),
        ("negative_controls", negative_controls),
        ("cookie_source_records", cookie_source_records),
    ):
        if not path.is_file():
            errors.append(f"{key}: missing {path}")
            counts[key] = 0
            continue
        records = load_yaml_records(path)
        counts[key] = len(records)
        schema_key = "promoted_sources" if key == "cookie_source_records" else key
        _validate_records(records, SCHEMA_MAP[schema_key], key, errors)

    manifests = sorted(manifest_dir.glob("exp_stage4b_*.yaml")) if manifest_dir.is_dir() else []
    counts["disabled_manifests"] = len(manifests)
    if len(manifests) != 7:
        errors.append(f"manifest_dir: expected 7 disabled manifests, found {len(manifests)}")
    manifest_ids: set[str] = set()
    for path in manifests:
        payload = load_yaml_payload(path)
        _validate_one(payload, SCHEMA_MAP["disabled_manifest"], path.name, errors)
        manifest_id = str(payload.get("manifest_id", ""))
        if manifest_id in manifest_ids:
            errors.append(f"{path.name}: duplicate manifest_id {manifest_id}")
        manifest_ids.add(manifest_id)
        if payload.get("execution_enabled") is not False:
            errors.append(f"{path.name}: execution_enabled must be false")
        if payload.get("cuda_enabled") is not False:
            errors.append(f"{path.name}: cuda_enabled must be false")
        if payload.get("no_solve_claim") is not True:
            errors.append(f"{path.name}: no_solve_claim must be true")

    _cross_record_checks(
        promoted_sources=load_yaml_records(promoted_sources) if promoted_sources.is_file() else [],
        visual_observations=load_yaml_records(visual_observations)
        if visual_observations.is_file()
        else [],
        negative_controls=load_yaml_records(negative_controls)
        if negative_controls.is_file()
        else [],
        errors=errors,
    )
    return counts, errors


def _cross_record_checks(
    *,
    promoted_sources: list[dict[str, Any]],
    visual_observations: list[dict[str, Any]],
    negative_controls: list[dict[str, Any]],
    errors: list[str],
) -> None:
    source_ids = {str(record.get("source_id")) for record in promoted_sources}
    for required in (
        "stage4b-rtkd-iddqd",
        "stage4b-scream314-cicada3301",
        "stage4b-complete-archive-magicsquares",
    ):
        if required not in source_ids:
            errors.append(f"promoted_sources: missing {required}")
    for record in visual_observations:
        if record.get("usable_as_experiment_seed") is not False:
            errors.append(
                f"{record.get('observation_id')}: usable_as_experiment_seed must be false"
            )
        if record.get("trusted_as_canonical") is not False:
            errors.append(f"{record.get('observation_id')}: trusted_as_canonical must be false")
        if record.get("solve_claim") is not False:
            errors.append(f"{record.get('observation_id')}: solve_claim must be false")
    negative_classes = {str(record.get("false_positive_class")) for record in negative_controls}
    for required in (
        "braille_dot_readings",
        "constellation_dot_readings",
        "broad_outguess_bruteforce_garbage",
        "attachment_reference_privacy_risk",
    ):
        if required not in negative_classes:
            errors.append(f"negative_controls: missing {required}")


def _validate_records(
    records: list[dict[str, Any]], schema_path: Path, label: str, errors: list[str]
) -> None:
    seen: set[str] = set()
    for record in records:
        _validate_one(record, schema_path, label, errors)
        identifier = _record_identifier(record)
        if identifier in seen:
            errors.append(f"{label}: duplicate id {identifier}")
        seen.add(identifier)
        if record.get("solve_claim") is not False:
            errors.append(f"{identifier}: solve_claim must be false")
        if record.get("trusted_as_canonical") is not False:
            errors.append(f"{identifier}: trusted_as_canonical must be false")
        if (
            record.get("classification") == "unsafe_or_private"
            and record.get("recommended_action") == "source-lock now"
        ):
            errors.append(f"{identifier}: unsafe/private links cannot be source-lock now")


def _record_identifier(record: dict[str, Any]) -> str:
    if "observation_id" in record:
        return str(record.get("observation_id"))
    if "negative_control_id" in record:
        return str(record.get("negative_control_id"))
    if "manifest_id" in record:
        return str(record.get("manifest_id"))
    return str(record.get("source_id", ""))


def _validate_one(
    payload: dict[str, Any], schema_path: Path, label: str, errors: list[str]
) -> None:
    schema = _load_schema(schema_path)
    try:
        validate(payload, schema)
    except ValidationError as error:
        errors.append(f"{label}: {error.message}")


def _load_schema(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
