"""Summary loading for Stage 4A full-review bundles."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.discord_full_review.export import read_json, resolve_path


def load_summary(results_dir: Path) -> dict[str, Any]:
    summary_path = resolve_path(results_dir) / "summary.json"
    if not summary_path.is_file():
        raise FileNotFoundError(summary_path)
    return read_json(summary_path)
