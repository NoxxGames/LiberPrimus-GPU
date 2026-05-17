"""Load Stage 2J bounded experiment queue records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.bounded_experiments.models import BoundedExperimentQueue
from libreprimus.bounded_experiments.validation import validate_queue_payload
from libreprimus.paths import repo_root
from libreprimus.transforms.registry import compute_sha256


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def load_bounded_queue(path: Path) -> BoundedExperimentQueue:
    resolved = _resolve(path)
    payload: Any = yaml.safe_load(resolved.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Bounded experiment queue must be a mapping: {resolved}")
    validate_queue_payload(payload)
    return BoundedExperimentQueue(payload=payload, path=str(resolved), sha256=compute_sha256(resolved))
