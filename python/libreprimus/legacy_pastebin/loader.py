"""Loader helpers for local legacy Pastebin text."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from libreprimus.paths import project_path

DEFAULT_INPUT_RELATIVE_PATHS = (
    Path("data/raw/legacy-pastebins/58-Pages-In-Runes-With-Prime-Values-Pastebin.txt"),
    Path("58-Pages-In-Runes-With-Prime-Values-Pastebin.txt"),
    Path("data/raw/legacy-pastebins/vGMK330j.txt"),
    Path("vGMK330j.txt"),
)


@dataclass(frozen=True)
class LoadedLegacyPastebin:
    path: Path
    sha256: str
    text: str


def default_input_candidates() -> list[Path]:
    """Return default local source paths in priority order."""
    return [project_path(str(path)) for path in DEFAULT_INPUT_RELATIVE_PATHS]


def find_default_input() -> Path | None:
    """Find the first present default local source path."""
    for path in default_input_candidates():
        if path.is_file():
            return path
    return None


def default_output_dir() -> Path:
    """Return the default generated output directory."""
    return project_path("data/normalized/legacy-pastebin")


def resolve_input_path(path: Path | None) -> Path:
    """Resolve an explicit or default local source path."""
    if path is not None:
        resolved = path if path.is_absolute() else project_path(str(path))
        if resolved.is_file():
            return resolved
        raise FileNotFoundError(f"Legacy Pastebin TXT source not found: {resolved}")

    found = find_default_input()
    if found is not None:
        return found

    searched = ", ".join(str(candidate) for candidate in default_input_candidates())
    raise FileNotFoundError(
        "Legacy Pastebin TXT source not found. No download was attempted. "
        f"Searched: {searched}"
    )


def compute_sha256(path: Path) -> str:
    """Compute SHA-256 for a local source file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_legacy_pastebin(path: Path) -> LoadedLegacyPastebin:
    """Load a local UTF-8 legacy Pastebin TXT source."""
    resolved = path.resolve()
    return LoadedLegacyPastebin(
        path=resolved,
        sha256=compute_sha256(resolved),
        text=resolved.read_text(encoding="utf-8-sig"),
    )
