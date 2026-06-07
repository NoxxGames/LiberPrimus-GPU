"""Manual override helpers for committed source-browser entries."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from ..settings import MANUAL_OVERRIDES_DIR
from .manual_entries import slugify


def override_path(target_entry_id: str) -> Path:
    return MANUAL_OVERRIDES_DIR / f"{slugify(target_entry_id)}.yaml"


def save_override(
    *,
    target_entry_id: str,
    target_source_record_path: str,
    fields: dict[str, Any],
) -> Path:
    MANUAL_OVERRIDES_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "record_type": "source_browser_manual_override",
        "schema": "schemas/operator-console/source-browser-manual-override-v0.schema.json",
        "target_entry_id": target_entry_id,
        "target_source_record_path": target_source_record_path,
        "modified_at": datetime.now(timezone.utc).isoformat(),
        "fields": fields,
        "solve_claim": False,
        "execution_allowed": False,
    }
    path = override_path(target_entry_id)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return path
