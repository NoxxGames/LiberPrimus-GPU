"""Summary loading for OutGuess regression outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.stego.outguess_export import read_json, resolve_path


def load_summary(results_dir: Path) -> dict[str, Any]:
    """Load an OutGuess regression summary."""
    return read_json(resolve_path(results_dir) / "summary.json")
