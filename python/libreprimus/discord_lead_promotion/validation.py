"""Validation for Stage 3R promoted records and manifests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.discord_lead_promotion.export import read_json, read_yaml
from libreprimus.discord_lead_promotion.manifest_builder import MANIFEST_FILENAMES
from libreprimus.paths import repo_root

FORBIDDEN_MARKERS = (
    "username:",
    "user_id:",
    "message_id:",
    "avatar_url:",
    "cdn.discordapp.com/attachments/",
    "media.discordapp.net/attachments/",
    "raw_message:",
    "message_body:",
)


def validate_stage3r_outputs(
    *,
    promoted_sources: Path,
    promoted_observations: Path,
    negative_controls: Path,
    manifest_dir: Path,
    allow_empty: bool = False,
) -> tuple[dict[str, int], list[str]]:
    """Validate committed Stage 3R records and disabled manifests."""
    errors: list[str] = []
    counts = {
        "promoted_source_count": 0,
        "promoted_observation_count": 0,
        "negative_control_count": 0,
        "manifest_count": 0,
    }
    schema_by_type = _load_schemas()
    source_records = _load_records(_resolve(promoted_sources), "sources", allow_empty, errors)
    observation_records = _load_records(_resolve(promoted_observations), "observations", allow_empty, errors)
    negative_records = _load_records(_resolve(negative_controls), "negative_controls", allow_empty, errors)
    counts["promoted_source_count"] = len(source_records)
    counts["promoted_observation_count"] = len(observation_records)
    counts["negative_control_count"] = len(negative_records)
    for record in source_records:
        _validate_record(schema_by_type["promoted_discord_source_record"], record, errors)
        _validate_privacy(record, errors, str(record.get("promoted_id")))
    for record in observation_records:
        _validate_record(schema_by_type["promoted_discord_observation_record"], record, errors)
        _validate_privacy(record, errors, str(record.get("observation_id")))
        if record.get("usable_as_experiment_seed") is not False:
            errors.append(f"{record.get('observation_id')}: usable_as_experiment_seed must be false")
    for record in negative_records:
        _validate_record(schema_by_type["negative_control_record"], record, errors)
        _validate_privacy(record, errors, str(record.get("negative_control_id")))
        if record.get("solve_claim") is not False:
            errors.append(f"{record.get('negative_control_id')}: solve_claim must be false")

    resolved_manifest_dir = _resolve(manifest_dir)
    for filename in MANIFEST_FILENAMES.values():
        path = resolved_manifest_dir / filename
        if not path.is_file():
            errors.append(f"missing manifest: {path}")
            continue
        payload = read_yaml(path)
        counts["manifest_count"] += 1
        _validate_record(schema_by_type["post_discord_experiment_manifest"], payload, errors)
        _validate_manifest_policy(payload, errors)
    _scan_files_for_forbidden_markers(
        [
            _resolve(promoted_sources),
            _resolve(promoted_observations),
            _resolve(negative_controls),
        ],
        errors,
    )
    return counts, errors


def _load_schemas() -> dict[str, dict[str, Any]]:
    paths = {
        "promoted_discord_source_record": "schemas/history/promoted-discord-source-record-v0.schema.json",
        "promoted_discord_observation_record": "schemas/history/promoted-discord-observation-record-v0.schema.json",
        "negative_control_record": "schemas/history/negative-control-record-v0.schema.json",
        "post_discord_experiment_manifest": "schemas/experiments/post-discord-experiment-manifest-v0.schema.json",
    }
    return {key: read_json(repo_root() / path) for key, path in paths.items()}


def _load_records(path: Path, label: str, allow_empty: bool, errors: list[str]) -> list[dict[str, Any]]:
    if not path.is_file():
        if allow_empty:
            return []
        errors.append(f"missing {label}: {path}")
        return []
    payload = read_yaml(path)
    records = payload.get("records", [])
    if not isinstance(records, list):
        errors.append(f"{label}: records must be a list")
        return []
    return [record for record in records if isinstance(record, dict)]


def _validate_record(schema: dict[str, Any], record: dict[str, Any], errors: list[str]) -> None:
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(record), key=str):
        errors.append(f"{record.get('record_type', 'record')}: {error.message}")


def _validate_privacy(record: dict[str, Any], errors: list[str], label: str) -> None:
    for field in ["raw_message_committed", "username_committed", "private_url_committed", "trusted_as_canonical"]:
        if record.get(field) is not False:
            errors.append(f"{label}: {field} must be false")


def _validate_manifest_policy(payload: dict[str, Any], errors: list[str]) -> None:
    label = str(payload.get("experiment_id"))
    expected_caps = {"EXP-3R-001": 576, "EXP-3R-003": 144, "EXP-3R-004": 64}
    if payload.get("candidate_count_cap") != expected_caps.get(label):
        errors.append(f"{label}: unexpected candidate_count_cap")
    for field, expected in {
        "execution_enabled": False,
        "cpu_only": True,
        "cuda_enabled": False,
        "cloud_execution": False,
        "paid_services": False,
        "generated_outputs_committed": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
    }.items():
        if payload.get(field) is not expected:
            errors.append(f"{label}: {field} must be {str(expected).lower()}")


def _scan_files_for_forbidden_markers(paths: list[Path], errors: list[str]) -> None:
    for path in paths:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8").lower()
        for marker in FORBIDDEN_MARKERS:
            if marker in text:
                errors.append(f"{path}: contains forbidden marker {marker}")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path
