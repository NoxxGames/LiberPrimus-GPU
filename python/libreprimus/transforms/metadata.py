"""Metadata helpers for CPU reference transform registry."""

from __future__ import annotations

from pathlib import Path

from libreprimus.paths import repo_root
from libreprimus.transforms.registry import DEFAULT_REGISTRY_PATH, compute_sha256


def registry_sha256(path: Path | None = None) -> str:
    return compute_sha256(path or repo_root() / DEFAULT_REGISTRY_PATH)
