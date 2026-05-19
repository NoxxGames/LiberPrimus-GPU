"""Summary loading for Stage 4G cookie refresh."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.cookie_refresh.models import DEFAULT_SUMMARY
from libreprimus.history.source_records import resolve_repo_path


def load_summary(path: Path = DEFAULT_SUMMARY) -> dict[str, Any]:
    """Load the committed Stage 4G aggregate summary."""

    payload = yaml.safe_load(resolve_repo_path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"summary must be a mapping: {path}")
    return payload
