"""Load committed observation families for Stage 4J review."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.observation_review.models import ObservationInput, SOURCE_RECORD_PATHS
from libreprimus.paths import repo_root


def load_yaml_records(path: Path) -> list[dict[str, Any]]:
    """Load a Stage-style YAML record set, singleton dict, or empty path."""

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


def write_yaml_document(path: Path, payload: dict[str, Any]) -> None:
    """Write a singleton YAML document."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")


def load_observation_inputs(root: Path | None = None) -> list[ObservationInput]:
    """Normalize committed observation records into review inputs."""

    base = root or repo_root()
    inputs: list[ObservationInput] = []
    for source_family, relative in SOURCE_RECORD_PATHS.items():
        path = base / relative
        for index, record in enumerate(load_yaml_records(path), start=1):
            observation_id = _record_id(record, source_family, index)
            inputs.append(
                ObservationInput(
                    source_family=source_family,
                    source_path=relative.as_posix(),
                    observation_id=observation_id,
                    observation_type=_observation_type(source_family, record),
                    payload=record,
                )
            )
    return inputs


def _record_id(record: dict[str, Any], source_family: str, index: int) -> str:
    for key in (
        "observation_id",
        "task_id",
        "candidate_id",
        "negative_control_id",
        "source_id",
        "fixture_id",
        "audio_fixture_id",
        "record_id",
        "experiment_id",
    ):
        value = record.get(key)
        if isinstance(value, str) and value:
            return value
    return f"{source_family}-{index}"


def _observation_type(source_family: str, record: dict[str, Any]) -> str:
    family = str(record.get("observation_family") or record.get("task_family") or record.get("false_positive_class") or "")
    record_type = str(record.get("record_type") or "")
    if "cuneiform" in source_family or "cuneiform" in family:
        return "visual_cuneiform_candidate"
    if "dot" in source_family or "dot" in family:
        return "visual_dot_pattern_candidate"
    if "delimiter" in source_family or "delimiter" in family:
        return "delimiter_candidate"
    if "negative" in source_family or record_type.endswith("negative_control_record"):
        return "negative_control"
    if "cookie" in source_family or "cookie" in family:
        return "cookie_hash_candidate"
    if source_family == "stage4b_sources":
        return "source_link"
    if "stego" in source_family or "outguess" in source_family or "audio" in source_family:
        return "stego_audio_fixture_candidate"
    if "image_artifact" in source_family or "compression" in family:
        return "image_compression_artifact_candidate"
    if "discord" in source_family:
        return "discord_derived_lead"
    if "number_square" in family or "numeric" in family:
        return "numeric_claim"
    if "gp" in family or "rune" in family:
        return "gp_rune_claim"
    return "numeric_claim"
