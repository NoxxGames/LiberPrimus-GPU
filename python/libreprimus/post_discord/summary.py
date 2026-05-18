"""Summary loading for Stage 3S post-Discord results."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.post_discord.export import read_json, resolve_path


def load_summary(results_dir: Path) -> dict[str, Any]:
    """Load a generated Stage 3S summary."""
    path = resolve_path(results_dir) / "summary.json"
    if not path.is_file():
        raise FileNotFoundError(f"Stage 3S summary not found: {path}")
    payload = read_json(path)
    if not isinstance(payload, dict):
        raise ValueError(f"Stage 3S summary must be a mapping: {path}")
    return payload
