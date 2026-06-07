"""Manual Source Browser entry helpers."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from ..settings import HUGE_TEXT_CHAR_LIMIT, HUGE_TEXT_LINE_LIMIT, MANUAL_ENTRIES_DIR


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower()).strip("_")
    return slug or "manual_entry"


def manual_entry_path(entry_id: str) -> Path:
    return MANUAL_ENTRIES_DIR / f"{slugify(entry_id)}.yaml"


def build_manual_entry(fields: dict[str, Any]) -> dict[str, Any]:
    created = str(fields.get("created_at") or now_iso())
    entry_id = str(fields.get("entry_id") or f"manual_{datetime.now(timezone.utc):%Y%m%d_%H%M%S}")
    return {
        "record_type": "source_browser_manual_entry",
        "schema": "schemas/operator-console/source-browser-manual-entry-v0.schema.json",
        "entry_id": entry_id,
        "created_at": created,
        "modified_at": str(fields.get("modified_at") or created),
        "created_by": str(fields.get("created_by") or "operator"),
        "category": str(fields.get("category") or "Manual entries"),
        "title": str(fields.get("title") or entry_id),
        "summary": str(fields.get("summary") or ""),
        "entry_type": str(fields.get("entry_type") or "manual_note"),
        "status": str(fields.get("status") or "review_note"),
        "trust_tier": str(fields.get("trust_tier") or "operator_local"),
        "confidence": str(fields.get("confidence") or "not_applicable"),
        "local_paths": _list(fields.get("local_paths")),
        "image_paths": _list(fields.get("image_paths")),
        "document_paths": _list(fields.get("document_paths")),
        "urls": _list(fields.get("urls")),
        "number_facts": _list(fields.get("number_facts")),
        "candidate_family_links": _list(fields.get("candidate_family_links") or fields.get("links_to")),
        "warnings": _list(fields.get("warnings")),
        "notes": str(fields.get("notes") or ""),
        "solve_claim": False,
        "execution_allowed": False,
    }


def save_manual_entry(fields: dict[str, Any]) -> Path:
    MANUAL_ENTRIES_DIR.mkdir(parents=True, exist_ok=True)
    payload = build_manual_entry(fields)
    errors = validate_no_huge_raw_blob(payload)
    if errors:
        raise ValueError("; ".join(errors))
    path = manual_entry_path(str(payload["entry_id"]))
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return path


def validate_no_huge_raw_blob(payload: Any) -> list[str]:
    errors: list[str] = []

    def visit(value: Any, path: str) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                visit(item, f"{path}.{key}" if path else str(key))
        elif isinstance(value, list):
            for index, item in enumerate(value):
                visit(item, f"{path}[{index}]")
        elif isinstance(value, str):
            if len(value) > HUGE_TEXT_CHAR_LIMIT:
                errors.append(f"{path} exceeds {HUGE_TEXT_CHAR_LIMIT} characters")
            if len(value.splitlines()) > HUGE_TEXT_LINE_LIMIT:
                errors.append(f"{path} exceeds {HUGE_TEXT_LINE_LIMIT} lines")

    visit(payload, "")
    return errors


def _list(value: Any) -> list[Any]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [item.strip() for item in value.splitlines() if item.strip()]
    return [value]
