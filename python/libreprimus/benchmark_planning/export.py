"""Export helpers for Stage 4Q benchmark planning."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from libreprimus.paths import repo_root


def resolve_repo_path(path: Path) -> Path:
    """Resolve a repository-relative path."""

    return path if path.is_absolute() else repo_root() / path


def write_json(path: Path, payload: Any) -> None:
    resolved = resolve_repo_path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    resolved = resolve_repo_path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records), encoding="utf-8")


def write_yaml(path: Path, payload: Any) -> None:
    resolved = resolve_repo_path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    resolved = resolve_repo_path(path)
    payload = json.loads(resolved.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON file must contain a mapping: {path}")
    return payload


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    resolved = resolve_repo_path(path)
    if not resolved.is_file():
        return []
    records: list[dict[str, Any]] = []
    for line in resolved.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        if not isinstance(payload, dict):
            raise ValueError(f"JSONL record must contain mappings: {path}")
        records.append(payload)
    return records


def read_yaml(path: Path) -> dict[str, Any]:
    resolved = resolve_repo_path(path)
    payload = yaml.safe_load(resolved.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"YAML file must contain a mapping: {path}")
    return payload
