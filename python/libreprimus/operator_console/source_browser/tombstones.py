"""Tombstone helpers for hiding committed records in the Source Browser."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import yaml

from ..settings import TOMBSTONES_DIR
from .manual_entries import slugify


def tombstone_path(target_entry_id: str) -> Path:
    return TOMBSTONES_DIR / f"{slugify(target_entry_id)}.yaml"


def save_tombstone(
    *,
    target_entry_id: str,
    target_source_record_path: str,
    reason: str = "hidden_by_operator",
) -> Path:
    TOMBSTONES_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "record_type": "source_browser_tombstone",
        "schema": "schemas/operator-console/source-browser-tombstone-v0.schema.json",
        "target_entry_id": target_entry_id,
        "target_source_record_path": target_source_record_path,
        "reason": reason,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "solve_claim": False,
        "execution_allowed": False,
    }
    path = tombstone_path(target_entry_id)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return path
