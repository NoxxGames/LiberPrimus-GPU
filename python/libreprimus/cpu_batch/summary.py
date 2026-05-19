"""Summary helpers for CPU batch generated outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from libreprimus.history.source_records import resolve_repo_path


def load_generated_summary(results_dir: Path) -> dict[str, Any]:
    """Load generated `summary.json` from a results directory."""

    path = resolve_repo_path(results_dir) / "summary.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"CPU batch summary must be a mapping: {path}")
    return payload


def load_committed_summary(path: Path) -> dict[str, Any]:
    """Load the committed Stage 4H aggregate summary."""

    payload = yaml.safe_load(resolve_repo_path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"committed summary must be a mapping: {path}")
    return payload
