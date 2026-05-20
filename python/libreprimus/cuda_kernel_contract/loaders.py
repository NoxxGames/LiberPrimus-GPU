"""Load committed Stage 5E input records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, resolve_repo_path


def load_records(path: Path) -> list[dict[str, Any]]:
    payload = read_yaml(path)
    records = payload.get("records")
    if not isinstance(records, list):
        raise ValueError(f"YAML file must contain a records list: {path}")
    return [record for record in records if isinstance(record, dict)]


def load_mapping(path: Path) -> dict[str, Any]:
    return read_yaml(path)


def optional_file_present(path: Path) -> bool:
    return resolve_repo_path(path).is_file()
