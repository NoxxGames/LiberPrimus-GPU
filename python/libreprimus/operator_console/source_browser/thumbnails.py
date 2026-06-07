"""Thumbnail helpers for local image display."""

from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image

from ..settings import THUMBNAIL_CACHE_DIR


def thumbnail_path(source_path: Path, size: tuple[int, int] = (128, 128)) -> Path:
    key = hashlib.sha256(str(source_path.resolve()).encode("utf-8")).hexdigest()[:16]
    return THUMBNAIL_CACHE_DIR / f"{key}_{size[0]}x{size[1]}.png"


def build_thumbnail(source_path: Path, size: tuple[int, int] = (128, 128)) -> Path | None:
    if not source_path.exists():
        return None
    THUMBNAIL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    target = thumbnail_path(source_path, size)
    if target.exists():
        return target
    with Image.open(source_path) as image:
        image.thumbnail(size)
        image.save(target)
    return target
