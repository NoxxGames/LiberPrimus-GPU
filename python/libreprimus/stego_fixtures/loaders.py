"""Load Stage 4F source metadata inputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_yaml_records(path: Path) -> list[dict[str, Any]]:
    """Load records from a YAML record set or single dict."""

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


def stage4e_candidates(stage4e_source_delta: Path) -> list[dict[str, Any]]:
    """Return selected Stage 4E path candidates from source-delta records."""

    candidates: list[dict[str, Any]] = []
    for record in load_yaml_records(stage4e_source_delta):
        selected = record.get("selected_path_candidates", [])
        if isinstance(selected, list):
            candidates.extend(candidate for candidate in selected if isinstance(candidate, dict))
    return candidates


def find_stage4b_source(stage4b_sources: list[dict[str, Any]], source_id: str) -> dict[str, Any] | None:
    """Find a Stage 4B source by source id."""

    for record in stage4b_sources:
        if record.get("source_id") == source_id:
            return record
    return None
