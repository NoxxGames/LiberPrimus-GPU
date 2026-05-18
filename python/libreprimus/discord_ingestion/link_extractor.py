"""URL extraction and classification for local Discord HTML exports."""

from __future__ import annotations

import hashlib
from pathlib import PurePosixPath
import re
from urllib.parse import urlparse

from libreprimus.discord_ingestion.models import ARCHIVE_ID
from libreprimus.discord_ingestion.redaction import normalize_url, redacted_url_for_record

URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.IGNORECASE)
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tif", ".tiff", ".svg"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".ogg", ".m4a"}
HTML_EXTENSIONS = {".html", ".htm"}


def extract_plaintext_urls(text: str) -> list[str]:
    return [match.group(0).strip("\"'<>),.;") for match in URL_RE.finditer(text)]


def classify_url(url: str) -> str:
    normalized = normalize_url(url)
    try:
        parsed = urlparse(normalized)
    except ValueError:
        return "unknown"
    domain = parsed.netloc.lower()
    suffix = PurePosixPath(parsed.path).suffix.lower()
    if "github.com" in domain or domain.endswith("githubusercontent.com"):
        return "github"
    if "fandom.com" in domain or "wikia.com" in domain:
        return "fandom"
    if "reddit.com" in domain or domain == "redd.it":
        return "reddit"
    if "pastebin.com" in domain:
        return "pastebin"
    if "docs.google.com" in domain or "drive.google.com" in domain:
        return "google_docs"
    if "archive.org" in domain or "web.archive.org" in domain:
        return "internet_archive"
    if "discordapp" in domain or "discord.com" in domain or "discordapp.net" in domain:
        return "discord_attachment"
    if suffix in IMAGE_EXTENSIONS:
        return "image"
    if suffix in AUDIO_EXTENSIONS:
        return "audio"
    if suffix == ".pdf":
        return "pdf"
    if suffix in HTML_EXTENSIONS:
        return "html"
    return "unknown"


def domain_for_url(url: str) -> str:
    try:
        return urlparse(normalize_url(url)).netloc.lower()
    except ValueError:
        return ""


def link_record(url: str, *, source_file_sha256: str, ordinal: int) -> dict:
    normalized = normalize_url(url)
    safe_url = redacted_url_for_record(url)
    link_id = hashlib.sha256(f"{source_file_sha256}:{ordinal}:{normalized}".encode("utf-8")).hexdigest()[:24]
    return {
        "record_type": "discord_extracted_link",
        "link_id": f"discord-link-{link_id}",
        "archive_id": ARCHIVE_ID,
        "source_file_sha256": source_file_sha256,
        "url": safe_url,
        "normalized_url": normalized,
        "domain": domain_for_url(normalized),
        "url_kind": classify_url(normalized),
        "surrounding_text_redacted": True,
        "message_body_committed": False,
        "review_status": "machine_checked",
        "notes": "Extracted from admin-provided local Discord HTML; message context is not committed.",
    }
