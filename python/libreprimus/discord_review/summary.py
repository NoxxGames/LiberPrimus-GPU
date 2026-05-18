"""Summary helpers for Stage 3Q Discord review bundles."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.paths import repo_root


def load_summary(results_dir: Path, aggregate: Path | None = None) -> dict[str, Any]:
    resolved_results = _resolve(results_dir)
    summary_path = resolved_results / "review_bundle_summary.json"
    if summary_path.is_file():
        return json.loads(summary_path.read_text(encoding="utf-8"))
    if aggregate is not None and _resolve(aggregate).is_file():
        import yaml

        payload = yaml.safe_load(_resolve(aggregate).read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            return payload
    raise FileNotFoundError(summary_path)


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path
