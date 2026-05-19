"""Discord image-reference helpers."""

from __future__ import annotations

from pathlib import Path

from libreprimus.discord_full_review.models import IMAGE_SUFFIXES


def media_kind_from_name(name: str) -> str:
    suffix = Path(name).suffix.lower()
    if suffix in IMAGE_SUFFIXES:
        return "image"
    if suffix in {".mp3", ".wav", ".ogg", ".flac"}:
        return "audio"
    if suffix in {".txt", ".md", ".pdf"}:
        return "document"
    return "attachment"
