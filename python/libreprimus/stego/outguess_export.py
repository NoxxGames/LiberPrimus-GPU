"""Output helpers for Stage 3V OutGuess regression."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.paths import repo_root
from libreprimus.solved_fixtures.models import to_jsonable


def resolve_path(path: Path | str) -> Path:
    """Resolve a path relative to the repository root."""
    candidate = Path(path)
    return candidate if candidate.is_absolute() else repo_root() / candidate


def write_json(path: Path, payload: Any) -> Path:
    """Write deterministic JSON."""
    resolved = resolve_path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(json.dumps(to_jsonable(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return resolved


def read_json(path: Path) -> dict[str, Any]:
    """Read deterministic JSON."""
    return json.loads(resolve_path(path).read_text(encoding="utf-8"))


def write_jsonl(path: Path, records: list[Any]) -> Path:
    """Write deterministic JSONL records."""
    resolved = resolve_path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(to_jsonable(record), sort_keys=True) for record in records]
    resolved.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return resolved
