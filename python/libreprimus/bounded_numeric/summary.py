"""Summary helpers for Stage 4D bounded numeric outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.bounded_numeric.loaders import read_json


def summarize_results(results_dir: Path) -> dict[str, Any]:
    """Load the generated Stage 4D summary."""

    return read_json(results_dir / "summary.json")
