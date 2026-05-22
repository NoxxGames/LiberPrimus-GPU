"""Load Stage 5AB document-staleness source-of-truth records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.doc_staleness.models import (
    DEFAULT_OPERATIONAL_FILE_MAP,
    DEFAULT_OPERATIONAL_PATHS,
    DEFAULT_SOURCE_OF_TRUTH,
    SourceOfTruth,
)
from libreprimus.paths import repo_root


def load_source_of_truth(path: Path | str | None = None, *, root: Path | None = None) -> SourceOfTruth:
    base = root or repo_root()
    resolved = _resolve(base, path or DEFAULT_SOURCE_OF_TRUTH)
    payload = yaml.safe_load(resolved.read_text(encoding="utf-8")) or {}
    return SourceOfTruth.from_dict(payload)


def load_operational_paths(
    path: Path | str | None = None,
    *,
    root: Path | None = None,
) -> tuple[str, ...]:
    base = root or repo_root()
    resolved = _resolve(base, path or DEFAULT_OPERATIONAL_FILE_MAP)
    if not resolved.is_file():
        return DEFAULT_OPERATIONAL_PATHS
    payload: dict[str, Any] = yaml.safe_load(resolved.read_text(encoding="utf-8")) or {}
    paths: list[str] = []
    for record in payload.get("records", []):
        if not isinstance(record, dict):
            continue
        level = str(record.get("staleness_check_level", "")).lower()
        if level in {"strict", "current_state", "mirror"}:
            paths.append(str(record["path"]))
    return tuple(dict.fromkeys(paths or DEFAULT_OPERATIONAL_PATHS))


def _resolve(root: Path, path: Path | str) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return root / candidate
