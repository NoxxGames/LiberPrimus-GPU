"""Hashing helpers for Stage 5AN generated private content."""

from __future__ import annotations

import hashlib
from pathlib import Path

from .inputs import resolve


def sha256_file(path: Path) -> str:
    """Return a SHA-256 digest for a file."""

    digest = hashlib.sha256()
    with resolve(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def dir_size_bytes(path: Path) -> int:
    """Return total bytes under a directory."""

    root = resolve(path)
    return sum(item.stat().st_size for item in root.rglob("*") if item.is_file())


def file_count(path: Path) -> int:
    """Return file count under a directory."""

    root = resolve(path)
    return sum(1 for item in root.rglob("*") if item.is_file())
