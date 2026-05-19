"""Load and write Stage 4N stego/audio readiness records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


class _NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data: object) -> bool:
        return True


def load_yaml_records(path: Path) -> list[dict[str, Any]]:
    """Load a Stage-style YAML record set, singleton YAML document, or absent path."""

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
        yaml.dump(
            {"record_set_id": record_set_id, "schema": schema, "records": records},
            sort_keys=False,
            allow_unicode=False,
            Dumper=_NoAliasDumper,
        ),
        encoding="utf-8",
    )


def write_yaml_document(path: Path, payload: dict[str, Any]) -> None:
    """Write a singleton YAML document."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.dump(payload, sort_keys=False, allow_unicode=False, Dumper=_NoAliasDumper), encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any] | list[dict[str, Any]]) -> None:
    """Write generated JSON output."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    """Write generated JSONL output."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records), encoding="utf-8")
