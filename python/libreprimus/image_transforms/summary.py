"""Summary loading for Stage 3P image transform outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.image_transforms.export import read_json
from libreprimus.paths import repo_root


def load_summary(results_dir: Path) -> dict[str, Any]:
    path = results_dir if results_dir.is_absolute() else repo_root() / results_dir
    return read_json(path / "summary.json")
