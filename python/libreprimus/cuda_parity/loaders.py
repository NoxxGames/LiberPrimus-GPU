"""Record loaders for Stage 5B CUDA parity harness generation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml


def load_records(path: Path) -> list[dict[str, Any]]:
    """Load a YAML mapping containing a ``records`` list."""

    records = read_yaml(path).get("records", [])
    if not isinstance(records, list):
        raise ValueError(f"records must be a list: {path}")
    return [dict(record) for record in records if isinstance(record, dict)]


def load_mapping(path: Path) -> dict[str, Any]:
    """Load a YAML mapping."""

    return read_yaml(path)


def record_by(records: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    """Index records by a string key."""

    return {str(record.get(key)): record for record in records if record.get(key)}
