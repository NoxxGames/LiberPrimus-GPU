"""Read/write helpers for Stage 5AC reporting records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from libreprimus.paths import repo_root


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def read_yaml(path: Path) -> Any:
    return yaml.safe_load(resolve(path).read_text(encoding="utf-8"))


def read_records(path: Path) -> list[dict[str, Any]]:
    payload = read_yaml(path)
    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        return [dict(record) for record in payload["records"] if isinstance(record, dict)]
    if isinstance(payload, list):
        return [dict(record) for record in payload if isinstance(record, dict)]
    raise ValueError(f"record file has no records list: {path}")


def write_records(path: Path, records: list[dict[str, Any]]) -> None:
    target = resolve(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(yaml.safe_dump({"records": records}, sort_keys=False), encoding="utf-8")


def write_summary(path: Path, payload: dict[str, Any]) -> None:
    target = resolve(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def write_json_report(out_dir: Path, filename: str, payload: Any) -> None:
    target = resolve(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    (target / filename).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_warnings(out_dir: Path, warnings: list[str]) -> None:
    target = resolve(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps({"warning": warning}, sort_keys=True) + "\n" for warning in warnings)
    (target / "warnings.jsonl").write_text(text, encoding="utf-8")


__all__ = ["read_records", "read_yaml", "resolve", "write_json_report", "write_records", "write_summary", "write_warnings"]
