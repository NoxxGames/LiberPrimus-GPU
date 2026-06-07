"""Load Source Browser records from committed metadata and manual records."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .entries import SourceBrowserEntry
from .normalizer import context_entry, normalize_record
from ..resources import ensure_default_configs
from ..settings import CONTEXT_FILE, MANUAL_RECORD_GLOBS, REPO_ROOT, SOURCE_RECORD_GLOBS


@dataclass
class SourceIndex:
    entries: list[SourceBrowserEntry] = field(default_factory=list)
    scanned_paths: list[str] = field(default_factory=list)
    parse_errors: list[str] = field(default_factory=list)

    def to_cache_payload(self) -> dict[str, Any]:
        return {
            "records_scanned": len(self.scanned_paths),
            "entries_loaded": len(self.entries),
            "parse_error_count": len(self.parse_errors),
            "parse_errors": self.parse_errors,
            "entries": [entry.to_dict(include_raw=False) for entry in self.entries],
        }


def load_record_file(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        payload = json.loads(text)
    else:
        payload = yaml.safe_load(text)
    if not isinstance(payload, dict):
        raise ValueError(f"{path.as_posix()} did not parse to a mapping")
    return payload


def iter_record_paths(include_manual: bool = True) -> list[Path]:
    paths: list[Path] = []
    for pattern in SOURCE_RECORD_GLOBS:
        paths.extend(Path.cwd().glob(pattern))
    if include_manual:
        for pattern in MANUAL_RECORD_GLOBS:
            paths.extend(Path.cwd().glob(pattern))
    return sorted(path for path in paths if path.is_file())


def build_source_index(include_manual: bool = True, include_context: bool = True) -> SourceIndex:
    ensure_default_configs()
    index = SourceIndex()
    for path in iter_record_paths(include_manual=include_manual):
        rel_path = _relative(path)
        index.scanned_paths.append(rel_path)
        try:
            payload = load_record_file(path)
            index.entries.append(normalize_record(Path(rel_path), payload))
        except Exception as exc:  # pragma: no cover - covered by validation result text
            index.parse_errors.append(f"{rel_path}: {exc}")
    if include_context:
        index.entries.append(context_entry(CONTEXT_FILE))
    index.entries.sort(key=lambda entry: (entry.stage_id or "", entry.category, entry.title, entry.entry_id))
    return index


def write_index_cache(path: Path, index: SourceIndex) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(index.to_cache_payload(), indent=2, sort_keys=True), encoding="utf-8")


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()
