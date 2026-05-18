"""Summary loading for Stage 3N Discord ingestion."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.discord_ingestion.export import read_json
from libreprimus.paths import repo_root


def load_summary(results_dir: Path) -> dict[str, Any]:
    """Load the generated Discord ingestion summary."""
    resolved = results_dir if results_dir.is_absolute() else repo_root() / results_dir
    path = resolved / "discord_ingestion_summary.json"
    if not path.is_file():
        raise FileNotFoundError(path)
    return read_json(path)
