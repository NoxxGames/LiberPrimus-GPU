"""Read/write helpers for Stage 5AF source-harvester records."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import yaml

from libreprimus.paths import repo_root


def resolve(path: Path) -> Path:
    """Resolve a repository-relative path."""

    return path if path.is_absolute() else repo_root() / path


def repo_relative(path: Path) -> str:
    """Return a best-effort repository-relative path string."""

    resolved = resolve(path)
    try:
        return resolved.relative_to(repo_root()).as_posix()
    except ValueError:
        return resolved.as_posix()


def read_yaml(path: Path) -> Any:
    """Read a YAML document."""

    return yaml.safe_load(resolve(path).read_text(encoding="utf-8"))


def read_records(path: Path) -> list[dict[str, Any]]:
    """Read a YAML record file using either records-list or bare-list shape."""

    payload = read_yaml(path)
    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        return [dict(record) for record in payload["records"] if isinstance(record, dict)]
    if isinstance(payload, list):
        return [dict(record) for record in payload if isinstance(record, dict)]
    raise ValueError(f"record file has no records list: {path}")


def write_yaml(path: Path, payload: Any) -> None:
    """Write a YAML document."""

    target = resolve(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def write_records(path: Path, records: list[dict[str, Any]], **header: Any) -> None:
    """Write a records YAML document."""

    write_yaml(path, {**header, "records": records})


def write_json(path: Path, payload: Any) -> None:
    """Write a deterministic JSON document."""

    target = resolve(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    """Write a deterministic JSONL file."""

    target = resolve(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records), encoding="utf-8")


def write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    """Write records as CSV."""

    target = resolve(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for record in records for key in record})
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def write_inventory(path: Path, records: list[dict[str, Any]]) -> None:
    """Write inventory records to JSONL or CSV based on file extension."""

    if path.suffix.lower() == ".csv":
        write_csv(path, records)
    else:
        write_jsonl(path, records)
