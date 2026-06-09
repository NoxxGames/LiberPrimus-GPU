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


@dataclass(frozen=True)
class PathResolution:
    path_text: str
    resolved_path: Path
    exists: bool
    source: str


class PathResolutionCache:
    """Cache source-browser path resolution and existence checks."""

    def __init__(self, aliases: list[PathAlias] | None = None) -> None:
        self.aliases = aliases if aliases is not None else load_path_aliases()
        self._cache: dict[str, PathResolution] = {}
        self.exists_checks = 0

    def resolve(self, path_text: str) -> PathResolution:
        normalized = path_text.replace("\\", "/")
        cached = self._cache.get(normalized)
        if cached is not None:
            return cached
        resolved, source = _resolve_with_source(normalized, self.aliases)
        self.exists_checks += 1
        result = PathResolution(
            path_text=normalized,
            resolved_path=resolved,
            exists=resolved.exists(),
            source=source,
        )
        self._cache[normalized] = result
        return result

    def path(self, path_text: str) -> Path:
        return self.resolve(path_text).resolved_path


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
    resolved, _source = _resolve_with_source(normalized, aliases or load_path_aliases())
    return resolved


def _resolve_with_source(path_text: str, aliases: list[PathAlias]) -> tuple[Path, str]:
    normalized = path_text.replace("\\", "/")
    path = Path(path_text)
    if path.is_absolute():
        return path, "absolute"
    candidate = REPO_ROOT / path
    if candidate.exists():
        return candidate, "repo_relative"
    alias_candidate: Path | None = None
    for alias in aliases or load_path_aliases():
        if normalized == alias.source_prefix or normalized.startswith(f"{alias.source_prefix}/"):
            suffix = normalized[len(alias.source_prefix) :].lstrip("/")
            target = Path(alias.target_prefix)
            if not target.is_absolute():
                target = REPO_ROOT / target
            resolved = target / suffix
            if resolved.exists():
                return resolved, "alias"
            alias_candidate = alias_candidate or resolved
    archive_candidate = _resolve_archive_relative(normalized)
    if archive_candidate is not None:
        return archive_candidate, "archive_relative"
    if alias_candidate is not None:
        return alias_candidate, "alias_missing"
    return candidate, "repo_relative_missing"


def _resolve_archive_relative(normalized_path: str) -> Path | None:
    first_part = normalized_path.split("/", 1)[0]
    if first_part not in ARCHIVE_RELATIVE_PREFIXES:
        return None
    for root in ARCHIVE_RELATIVE_ROOTS:
        candidate = REPO_ROOT / root / normalized_path
        if candidate.exists():
            return candidate
    return None
