"""Input loading helpers for Stage 3P image transforms."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image

from libreprimus.image_transforms.models import IMAGE_SUFFIXES
from libreprimus.paths import repo_root


def iter_image_paths(source_dir: Path) -> list[Path]:
    """Return sorted local image files under source_dir."""
    return sorted(
        path
        for path in source_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    )


def load_image(path: Path) -> Image.Image:
    """Load a local image fully and detach it from the source file."""
    with Image.open(path) as image:
        image.load()
        return image.copy()


def load_image_locks(path: Path) -> dict[str, dict[str, Any]]:
    """Load Stage 3K image lock JSONL records by relative path."""
    if not path.is_file():
        return {}
    locks: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            record = json.loads(stripped)
            relative_path = str(record.get("relative_path", ""))
            if relative_path:
                locks[relative_path] = record
    return locks


def display_path(path: Path) -> str:
    """Return a repo-relative path for generated records when possible."""
    try:
        return path.resolve().relative_to(repo_root()).as_posix()
    except ValueError:
        return path.as_posix()
