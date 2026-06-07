"""Path-alias loading and resolution."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from ..settings import DEFAULT_PATH_ALIASES, REPO_ROOT


@dataclass(frozen=True)
class PathAlias:
    source_prefix: str
    target_prefix: str


def load_path_aliases(path: Path = DEFAULT_PATH_ALIASES) -> list[PathAlias]:
    if not path.exists():
        return []
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    aliases: list[PathAlias] = []
    for item in payload.get("path_aliases", []):
        if isinstance(item, dict) and item.get("from") and item.get("to"):
            aliases.append(PathAlias(str(item["from"]).replace("\\", "/"), str(item["to"])))
    return aliases


def resolve_with_aliases(path_text: str, aliases: list[PathAlias] | None = None) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    candidate = REPO_ROOT / path
    if candidate.exists():
        return candidate
    for alias in aliases or load_path_aliases():
        normalized = path_text.replace("\\", "/")
        if normalized == alias.source_prefix or normalized.startswith(f"{alias.source_prefix}/"):
            suffix = normalized[len(alias.source_prefix) :].lstrip("/")
            target = Path(alias.target_prefix)
            if not target.is_absolute():
                target = REPO_ROOT / target
            return target / suffix
    return candidate
