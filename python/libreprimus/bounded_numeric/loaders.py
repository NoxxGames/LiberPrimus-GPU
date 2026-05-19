"""Load and write Stage 4D bounded numeric records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def load_yaml_payload(path: Path) -> dict[str, Any]:
    """Load one YAML mapping from disk."""

    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected YAML mapping: {path}")
    return payload


def load_yaml_records(path: Path) -> list[dict[str, Any]]:
    """Load a committed record-set YAML file."""

    payload = load_yaml_payload(path)
    records = payload.get("records", [])
    if not isinstance(records, list):
        raise ValueError(f"records must be a list: {path}")
    return [dict(item) for item in records if isinstance(item, dict)]


def write_json(path: Path, payload: dict[str, Any]) -> Path:
    """Write a deterministic JSON mapping."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def read_json(path: Path) -> dict[str, Any]:
    """Read a JSON mapping from disk."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON mapping: {path}")
    return payload


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> Path:
    """Write newline-delimited JSON records."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
    return path


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Read newline-delimited JSON records."""

    records: list[dict[str, Any]] = []
    if not path.is_file():
        return records
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            payload = json.loads(line)
            if isinstance(payload, dict):
                records.append(payload)
    return records
