"""Summary loader for generated hash-preimage runs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.history.source_records import resolve_repo_path


def load_summary(results_dir: Path) -> dict[str, Any]:
    path = resolve_repo_path(results_dir) / "summary.json"
    return json.loads(path.read_text(encoding="utf-8"))
