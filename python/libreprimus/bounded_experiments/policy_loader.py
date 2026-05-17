"""Load Stage 2J operator-policy records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.bounded_experiments.models import OperatorPolicy
from libreprimus.bounded_experiments.validation import validate_operator_policy_payload
from libreprimus.paths import repo_root
from libreprimus.transforms.registry import compute_sha256


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def load_operator_policy(path: Path) -> OperatorPolicy:
    resolved = _resolve(path)
    payload: Any = yaml.safe_load(resolved.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Operator policy must be a mapping: {resolved}")
    validate_operator_policy_payload(payload)
    return OperatorPolicy(payload=payload, path=str(resolved), sha256=compute_sha256(resolved))
