"""Validation for Stage 3O promoted Discord source records."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from libreprimus.discord_promotion.export import read_yaml
from libreprimus.paths import repo_root

FORBIDDEN_MARKERS = (
    "message_body:",
    "raw_message:",
    "username:",
    "user_id:",
    "message_id:",
    "avatar:",
    "cdn.discordapp.com/attachments",
    "media.discordapp.net/attachments",
)


def validate_promoted_records(
    *,
    links: Path,
    methods: Path,
    numerics: Path,
    allow_empty: bool = False,
) -> tuple[dict[str, int], list[str]]:
    """Validate committed Stage 3O promotion records."""
    errors: list[str] = []
    payloads = {
        "links": _load_or_empty(links, allow_empty),
        "methods": _load_or_empty(methods, allow_empty),
        "numerics": _load_or_empty(numerics, allow_empty),
    }
    counts: dict[str, int] = {}
    for name, payload in payloads.items():
        records = payload.get("records", [])
        if not isinstance(records, list):
            errors.append(f"{name}: records must be a list")
            records = []
        counts[f"{name}_count"] = len(records)
        for record in records:
            if not isinstance(record, dict):
                errors.append(f"{name}: record must be mapping")
                continue
            _validate_record(name, record, errors)
        source_path = _resolve({"links": links, "methods": methods, "numerics": numerics}[name])
        text = source_path.read_text(encoding="utf-8") if source_path.is_file() else ""
        lower_text = text.lower()
        for marker in FORBIDDEN_MARKERS:
            if marker in lower_text:
                errors.append(f"{name}: forbidden marker {marker}")
    return counts, errors


def _load_or_empty(path: Path, allow_empty: bool) -> dict[str, Any]:
    resolved = _resolve(path)
    if allow_empty and not resolved.is_file():
        return {"records": []}
    return read_yaml(resolved)


def _validate_record(name: str, record: dict[str, Any], errors: list[str]) -> None:
    record_id = record.get("promoted_id", "<unknown>")
    if record.get("source") != "discord_admin_export_stage3n":
        errors.append(f"{name}:{record_id}: invalid source")
    if record.get("redacted") is not True:
        errors.append(f"{name}:{record_id}: redacted must be true")
    if record.get("trusted_as_canonical") is not False:
        errors.append(f"{name}:{record_id}: trusted_as_canonical must be false")
    if record.get("raw_message_committed") is not False:
        errors.append(f"{name}:{record_id}: raw_message_committed must be false")
    if record.get("usernames_committed") is not False:
        errors.append(f"{name}:{record_id}: usernames_committed must be false")
    if not record.get("review_status"):
        errors.append(f"{name}:{record_id}: review_status is required")
    if name == "links":
        url = str(record.get("url", ""))
        try:
            domain = urlparse(url).netloc.lower()
        except ValueError:
            domain = ""
        if domain.startswith("discord") or ".discord" in domain or "?" in url or not url.startswith(("http://", "https://")):
            errors.append(f"{name}:{record_id}: promoted URL is not public-safe")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path
