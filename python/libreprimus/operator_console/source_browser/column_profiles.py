"""Column-profile helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from ..settings import DEFAULT_COLUMN_PROFILE


def load_column_profile(path: Path = DEFAULT_COLUMN_PROFILE) -> dict[str, Any]:
    if not path.exists():
        return {"profile_id": "default", "columns": []}
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        return {"profile_id": "default", "columns": []}
    return payload


def visible_columns(path: Path = DEFAULT_COLUMN_PROFILE) -> list[dict[str, Any]]:
    payload = load_column_profile(path)
    columns = payload.get("columns", [])
    return [column for column in columns if isinstance(column, dict) and column.get("key")]
