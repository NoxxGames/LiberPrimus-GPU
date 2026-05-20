"""Export helpers for Stage 5D native CPU records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from libreprimus.benchmark_planning.export import resolve_repo_path


def write_json(path: Path, payload: Any) -> None:
    resolved = resolve_repo_path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Any) -> None:
    resolved = resolve_repo_path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")


def write_warnings(path: Path, warnings: list[dict[str, str]]) -> None:
    resolved = resolve_repo_path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text("".join(json.dumps(item, sort_keys=True) + "\n" for item in warnings), encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(resolve_repo_path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON file must contain a mapping: {path}")
    return payload


def read_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(resolve_repo_path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"YAML file must contain a mapping: {path}")
    return payload
