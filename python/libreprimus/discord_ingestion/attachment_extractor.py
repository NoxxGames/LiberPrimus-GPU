"""Attachment candidate extraction from redacted link records."""

from __future__ import annotations

import hashlib
from pathlib import PurePosixPath
from urllib.parse import urlparse

from libreprimus.discord_ingestion.link_extractor import AUDIO_EXTENSIONS, IMAGE_EXTENSIONS
from libreprimus.discord_ingestion.models import ARCHIVE_ID

DOCUMENT_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"}
ARCHIVE_EXTENSIONS = {".zip", ".7z", ".rar", ".tar", ".gz"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm", ".mkv"}


def attachment_candidates_from_links(link_records: list[dict]) -> list[dict]:
    records: list[dict] = []
    for ordinal, link in enumerate(link_records):
        kind = _media_kind(link["normalized_url"], link["url_kind"])
        if kind == "unknown":
            continue
        parsed = _parse_url(link["normalized_url"])
        if parsed is None:
            continue
        file_name = PurePosixPath(parsed.path).name
        extension = PurePosixPath(parsed.path).suffix.lower()
        attachment_id = hashlib.sha256(
            f"{link['source_file_sha256']}:{ordinal}:{link['normalized_url']}".encode("utf-8")
        ).hexdigest()[:24]
        records.append(
            {
                "record_type": "discord_attachment_candidate",
                "attachment_id": f"discord-attachment-{attachment_id}",
                "archive_id": ARCHIVE_ID,
                "source_file_sha256": link["source_file_sha256"],
                "url_or_path_redacted": link["normalized_url"],
                "file_name": file_name,
                "extension": extension.lstrip("."),
                "media_kind": kind,
                "private_url_redacted": True,
                "review_status": "machine_checked",
                "notes": "Attachment candidate only; file was not fetched or copied.",
            }
        )
    return records


def _media_kind(url: str, url_kind: str) -> str:
    parsed = _parse_url(url)
    if parsed is None:
        return "unknown"
    suffix = PurePosixPath(parsed.path).suffix.lower()
    if url_kind == "discord_attachment" and not suffix:
        return "unknown"
    if url_kind == "image" or suffix in IMAGE_EXTENSIONS:
        return "image"
    if url_kind == "audio" or suffix in AUDIO_EXTENSIONS:
        return "audio"
    if suffix in VIDEO_EXTENSIONS:
        return "video"
    if url_kind == "pdf" or suffix in DOCUMENT_EXTENSIONS:
        return "document"
    if suffix in ARCHIVE_EXTENSIONS:
        return "archive"
    if url_kind == "html" or suffix in {".html", ".htm"}:
        return "html"
    return "unknown"


def _parse_url(url: str):
    try:
        return urlparse(url)
    except ValueError:
        return None
