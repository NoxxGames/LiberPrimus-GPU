"""Path-alias loading and resolution."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from ..settings import DEFAULT_PATH_ALIASES, REPO_ROOT

ARCHIVE_RELATIVE_ROOTS = (
    Path("third_party/CicadaSolversIddqd"),
    Path("third_party/The-Complete-Cicada3301-Archive-main"),
    Path("third_party/CicadaArchive"),
)
ARCHIVE_RELATIVE_PREFIXES = {
    "2012",
    "2013",
    "2014",
    "2015",
    "2016",
    "2017",
    "assets",
    "EXTRA WIKI PAGES",
}


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
    normalized = path_text.replace("\\", "/")
    path = Path(path_text)
    if path.is_absolute():
        return path
    candidate = REPO_ROOT / path
    if candidate.exists():
        return candidate
    alias_candidate: Path | None = None
    for alias in aliases or load_path_aliases():
        if normalized == alias.source_prefix or normalized.startswith(f"{alias.source_prefix}/"):
            suffix = normalized[len(alias.source_prefix) :].lstrip("/")
            target = Path(alias.target_prefix)
            if not target.is_absolute():
                target = REPO_ROOT / target
            resolved = target / suffix
            if resolved.exists():
                return resolved
            alias_candidate = alias_candidate or resolved
    archive_candidate = _resolve_archive_relative(normalized)
    if archive_candidate is not None:
        return archive_candidate
    if alias_candidate is not None:
        return alias_candidate
    return candidate


def _resolve_archive_relative(normalized_path: str) -> Path | None:
    first_part = normalized_path.split("/", 1)[0]
    if first_part not in ARCHIVE_RELATIVE_PREFIXES:
        return None
    for root in ARCHIVE_RELATIVE_ROOTS:
        candidate = REPO_ROOT / root / normalized_path
        if candidate.exists():
            return candidate
    return None
