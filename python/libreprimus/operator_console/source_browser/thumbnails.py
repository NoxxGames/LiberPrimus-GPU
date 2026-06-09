"""Thumbnail helpers for local image display."""

from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image

from ..settings import THUMBNAIL_CACHE_DIR


def thumbnail_path(source_path: Path, size: tuple[int, int] = (128, 128)) -> Path:
    try:
        stat = source_path.stat()
        stamp = f"{stat.st_size}:{stat.st_mtime_ns}"
    except OSError:
        stamp = "missing"
    key = hashlib.sha256(
        f"{source_path.resolve()}|{stamp}|{size[0]}x{size[1]}".encode("utf-8")
    ).hexdigest()[:16]
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


class ThumbnailCache:
    """Lazy thumbnail cache for selected-entry detail views."""

    def __init__(self, size: tuple[int, int] = (128, 128)) -> None:
        self.size = size
        self._cache: dict[Path, Path | None] = {}

    def get(self, source_path: Path) -> Path | None:
        cached = self._cache.get(source_path)
        if source_path in self._cache:
            return cached
        thumbnail = build_thumbnail(source_path, self.size)
        self._cache[source_path] = thumbnail
        return thumbnail
