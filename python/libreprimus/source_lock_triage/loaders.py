"""Loaders for Stage 4B YAML and JSONL records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_yaml_records(path: Path) -> list[dict[str, Any]]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("records"), list):
        raise ValueError(f"Expected records list in {path}")
    records = payload["records"]
    if not all(isinstance(record, dict) for record in records):
        raise ValueError(f"Every record must be a mapping in {path}")
    return records


def load_yaml_payload(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected mapping payload in {path}")
    return payload


def write_yaml_records(
    path: Path, *, record_set_id: str, schema: str, records: list[dict[str, Any]]
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"record_set_id": record_set_id, "schema": schema, "records": records}
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")
