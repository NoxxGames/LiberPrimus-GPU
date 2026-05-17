"""Load Stage 3E method backlog files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.method_backlog.models import MethodBacklog
from libreprimus.method_backlog.validation import validate_method_backlog
from libreprimus.paths import repo_root
from libreprimus.transforms.registry import compute_sha256


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def load_method_backlog(path: Path) -> MethodBacklog:
    resolved = _resolve(path)
    payload: Any = yaml.safe_load(resolved.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Method backlog must be a mapping: {resolved}")
    validate_method_backlog(payload)
    return MethodBacklog(payload=payload, path=str(resolved), sha256=compute_sha256(resolved))
