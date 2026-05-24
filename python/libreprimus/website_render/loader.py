"""Load Stage 5AL website-ingest metadata for Stage 5AM."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from libreprimus.paths import repo_root

from .models import SAFE_DATASETS


def resolve(path: Path) -> Path:
    """Resolve a repository-relative path."""

    return path if path.is_absolute() else repo_root() / path


def repo_relative(path: Path) -> str:
    """Return a repository-relative path when possible."""

    resolved = resolve(path)
    try:
        return resolved.relative_to(repo_root()).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> Any:
    """Read a JSON document."""

    return json.loads(resolve(path).read_text(encoding="utf-8"))


def read_yaml(path: Path) -> Any:
    """Read a YAML document."""

    return yaml.safe_load(resolve(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    """Write deterministic JSON."""

    target = resolve(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Any) -> None:
    """Write deterministic YAML."""

    target = resolve(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    """Write deterministic JSONL."""

    target = resolve(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records), encoding="utf-8")


def load_stage5al_inputs(website_ingest_dir: Path, stage5al_summary: Path) -> dict[str, Any]:
    """Load all committed Stage 5AL website-ingest JSON inputs."""

    root = resolve(website_ingest_dir)
    datasets = {name: read_json(root / filename) for name, filename in SAFE_DATASETS.items()}
    summary = read_yaml(stage5al_summary)
    if not isinstance(summary, dict):
        raise ValueError(f"Stage 5AL summary is not a mapping: {stage5al_summary}")
    return {
        "website_ingest_dir": repo_relative(website_ingest_dir),
        "stage5al_summary_path": repo_relative(stage5al_summary),
        "stage5al_summary": summary,
        "datasets": datasets,
    }


def records(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    """Return a records list from a Stage 5AL payload."""

    dataset = payload["datasets"][key]
    raw_records = dataset.get("records", []) if isinstance(dataset, dict) else []
    return [dict(record) for record in raw_records if isinstance(record, dict)]
