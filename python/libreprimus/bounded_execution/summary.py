"""Read generated Stage 3A bounded run summaries."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.paths import repo_root


def load_summary(results_dir: Path) -> dict[str, Any]:
    resolved = results_dir if results_dir.is_absolute() else repo_root() / results_dir
    path = resolved / "summary.json"
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Stage 3A summary must be a mapping: {path}")
    return payload
