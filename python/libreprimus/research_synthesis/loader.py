"""Load Stage 3Y research-synthesis YAML records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.paths import repo_root
from libreprimus.research_synthesis.models import RECORD_SET_SPECS, RecordSetSpec


def resolve_repo_path(path: Path) -> Path:
    """Resolve a repository-relative or absolute path."""

    return path if path.is_absolute() else repo_root() / path


def read_yaml(path: Path) -> dict[str, Any]:
    """Read a YAML mapping from disk."""

    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected YAML mapping: {path}")
    return payload


def load_record_set(data_dir: Path, spec: RecordSetSpec) -> list[dict[str, Any]]:
    """Load one record set by spec."""

    path = resolve_repo_path(data_dir) / spec.filename
    payload = read_yaml(path)
    records = payload.get("records")
    if not isinstance(records, list):
        raise ValueError(f"Expected records list in {path}")
    typed_records: list[dict[str, Any]] = []
    for record in records:
        if not isinstance(record, dict):
            raise ValueError(f"Expected mapping records in {path}")
        typed_records.append(record)
    return typed_records


def load_all_record_sets(data_dir: Path) -> dict[str, list[dict[str, Any]]]:
    """Load all Stage 3Y research-synthesis record sets."""

    return {spec.key: load_record_set(data_dir, spec) for spec in RECORD_SET_SPECS}
