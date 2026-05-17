"""Read generated Stage 2J bounded auto-run summaries."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.paths import repo_root


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def load_summary(results_dir: Path) -> dict[str, Any]:
    path = _resolve(results_dir) / "summary.json"
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Bounded auto-run summary must be a mapping: {path}")
    return payload


def load_results(results_dir: Path) -> list[dict[str, Any]]:
    resolved = _resolve(results_dir)
    results = []
    for path in sorted(resolved.glob("*-bounded-auto-run-result.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            results.append(payload)
    return results
