"""Output helpers for Stage 3S post-Discord experiments."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.paths import repo_root
from libreprimus.solved_fixtures.models import to_jsonable


def resolve_path(path: Path) -> Path:
    """Resolve a path relative to the repository root."""
    return path if path.is_absolute() else repo_root() / path


def write_json(path: Path, payload: Any) -> Path:
    """Write deterministic JSON."""
    resolved = resolve_path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(json.dumps(to_jsonable(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return resolved


def read_json(path: Path) -> dict[str, Any]:
    """Read deterministic JSON."""
    return json.loads(resolve_path(path).read_text(encoding="utf-8"))
