"""Export helpers for Stage 5G CUDA parity reporting records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, resolve_repo_path, write_json, write_yaml


def read_record_set(path: Path) -> list[dict[str, Any]]:
    payload = read_yaml(path)
    if not isinstance(payload, dict):
        raise ValueError(f"record set must be a mapping: {path}")
    records = payload.get("records", [])
    if not isinstance(records, list):
        raise ValueError(f"records must be a list: {path}")
    return list(records)


def write_record_set(path: Path, records: list[dict[str, Any]]) -> None:
    write_yaml(path, {"records": records})


def write_report(out_dir: Path, filename: str, payload: Any) -> None:
    write_json(resolve_repo_path(out_dir) / filename, payload)


def write_warnings(out_dir: Path, warnings: list[dict[str, Any]]) -> None:
    path = resolve_repo_path(out_dir) / "warnings.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(item, sort_keys=True) + "\n" for item in warnings), encoding="utf-8")
