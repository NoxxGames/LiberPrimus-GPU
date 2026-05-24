"""Input loading and deterministic read/write helpers for Stage 5AN."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from libreprimus.paths import repo_root


def resolve(path: Path) -> Path:
    """Resolve a repository-relative path."""

    return path if path.is_absolute() else repo_root() / path


def repo_relative(path: Path) -> str:
    """Return a repository-relative path string when possible."""

    resolved = resolve(path)
    try:
        return resolved.relative_to(repo_root()).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> Any:
    """Read JSON."""

    return json.loads(resolve(path).read_text(encoding="utf-8"))


def read_yaml(path: Path) -> Any:
    """Read YAML."""

    return yaml.safe_load(resolve(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    """Write deterministic JSON."""

    target = resolve(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    """Write deterministic JSONL."""

    target = resolve(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records), encoding="utf-8")


def write_yaml(path: Path, payload: Any) -> None:
    """Write deterministic YAML."""

    target = resolve(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def load_website_ingest(website_ingest_dir: Path) -> dict[str, Any]:
    """Load Stage 5AL website-ingest datasets."""

    root = resolve(website_ingest_dir)
    return {
        "research_index": read_json(root / "research-index.json"),
        "bundles": read_json(root / "research-bundles.json"),
        "source_cards": read_json(root / "source-cards.json"),
        "content": read_json(root / "content-index.json"),
        "claims": read_json(root / "community-claims.json"),
        "publication_gates": read_json(root / "publication-gates.json"),
        "missing_sources": read_json(root / "missing-sources.json"),
        "deep_research_export": read_json(root / "deep-research-export.json"),
        "summary": read_yaml(root / "summary.yaml"),
    }


def records(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    """Return a records list from a loaded Stage 5AL dataset."""

    dataset = payload.get(key, {})
    if isinstance(dataset, dict) and isinstance(dataset.get("records"), list):
        return [dict(record) for record in dataset["records"] if isinstance(record, dict)]
    return []


def ensure_clean_dir(path: Path) -> Path:
    """Create an output directory after removing previous generated contents."""

    import shutil

    target = resolve(path)
    if target.exists():
        if target == repo_root() or target.parent == target:
            raise ValueError(f"refusing to clear unsafe output directory: {target}")
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)
    return target
