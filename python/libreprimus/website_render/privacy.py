"""Privacy and publication-gate checks for static website exports."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .loader import resolve

ABSOLUTE_PATH_PATTERNS = [
    re.compile(r"\b[A-Za-z]:[\\/][^\s\"'<>]+"),
    re.compile(r"\\\\[A-Za-z0-9_.-]+\\[^\s\"'<>]+"),
    re.compile(r"/home/[^\s\"'<>]+"),
    re.compile(r"/mnt/[^\s\"'<>]+"),
    re.compile(r"/Users/[^\s\"'<>]+"),
]

PRIVATE_ID_PATTERNS = [
    re.compile(r"cdn\.discordapp\.com/attachments", re.IGNORECASE),
    re.compile(r"discord(?:app)?\.com/channels/\d{12,}", re.IGNORECASE),
    re.compile(r"(token|session|cookie|auth)[=:][A-Za-z0-9_.-]{12,}", re.IGNORECASE),
]

RAW_BODY_MARKERS = [
    "chatlog__message",
    "BEGIN RAW",
    "raw message body",
    "base64,",
]

FORBIDDEN_BODY_FIELDS = {
    "claim_text",
    "claim_formula",
    "claimed_values",
    "source_message_locator",
    "source_image_refs",
    "body",
    "raw_body",
    "raw_text",
    "extracted_text",
}


def sanitize_record(record: dict[str, Any]) -> dict[str, Any]:
    """Return a conservative metadata-only record for static export."""

    clean: dict[str, Any] = {}
    for key, value in sorted(record.items()):
        if key in FORBIDDEN_BODY_FIELDS:
            continue
        clean[key] = _sanitize_value(value)
    clean.setdefault("raw_bodies_included", False)
    clean.setdefault("private_ids_published", False)
    clean.setdefault("solve_claim", False)
    return clean


def sanitize_payload(payload: Any) -> Any:
    """Sanitize a Stage 5AL payload recursively."""

    if isinstance(payload, dict):
        if "records" in payload and isinstance(payload["records"], list):
            sanitized = {
                key: _sanitize_value(value)
                for key, value in sorted(payload.items())
                if key != "records" and key not in FORBIDDEN_BODY_FIELDS
            }
            sanitized["records"] = [sanitize_record(record) for record in payload["records"] if isinstance(record, dict)]
            return sanitized
        return {
            key: _sanitize_value(value)
            for key, value in sorted(payload.items())
            if key not in FORBIDDEN_BODY_FIELDS
        }
    if isinstance(payload, list):
        return [_sanitize_value(item) for item in payload]
    return payload


def audit_site(site_root: Path) -> dict[str, Any]:
    """Scan generated static files for privacy and publication hazards."""

    root = resolve(site_root)
    findings: list[dict[str, str]] = []
    scanned_files = 0
    if root.exists():
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".html", ".css", ".js", ".json", ".txt", ".md"}:
                findings.append({"path": path.relative_to(root).as_posix(), "finding": "unexpected_binary_or_unknown_file"})
                continue
            scanned_files += 1
            text = path.read_text(encoding="utf-8")
            rel = path.relative_to(root).as_posix()
            for pattern in ABSOLUTE_PATH_PATTERNS:
                if pattern.search(text):
                    findings.append({"path": rel, "finding": "local_absolute_path"})
            for pattern in PRIVATE_ID_PATTERNS:
                if pattern.search(text):
                    findings.append({"path": rel, "finding": "private_identifier_or_private_url"})
            for marker in RAW_BODY_MARKERS:
                if marker in text:
                    findings.append({"path": rel, "finding": "raw_body_marker"})
            if re.search(r"data:image/[^;]+;base64,", text, re.IGNORECASE):
                findings.append({"path": rel, "finding": "embedded_base64_image"})

    return {
        "record_type": "stage5am_privacy_publication_audit",
        "schema": "schemas/website-render/privacy-publication-audit-v0.schema.json",
        "stage_id": "stage-5am",
        "site_root": site_root.as_posix(),
        "metadata_only": True,
        "files_scanned": scanned_files,
        "finding_count": len(findings),
        "findings": findings,
        "privacy_audit_passed": not findings,
        "raw_bodies_included": False,
        "private_ids_published": False,
        "local_absolute_paths_published": False,
        "public_website_publication_performed": False,
        "solve_claim": False,
    }


def _sanitize_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            str(key): _sanitize_value(item)
            for key, item in sorted(value.items())
            if str(key) not in FORBIDDEN_BODY_FIELDS
        }
    if isinstance(value, list):
        return [_sanitize_value(item) for item in value]
    if isinstance(value, str):
        sanitized = value
        for pattern in ABSOLUTE_PATH_PATTERNS:
            sanitized = pattern.sub("[redacted-local-path]", sanitized)
        for pattern in PRIVATE_ID_PATTERNS:
            sanitized = pattern.sub("[redacted-private-reference]", sanitized)
        return sanitized
    return value
