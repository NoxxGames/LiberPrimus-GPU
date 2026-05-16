"""Path helpers for the legacy workbook importer."""

from __future__ import annotations

from pathlib import Path

from libreprimus.paths import project_path

DEFAULT_WORKBOOK_RELATIVE_PATHS = (
    Path("data/raw/legacy-workbooks/tranlsations.xlsx"),
    Path("tranlsations.xlsx"),
)


def default_workbook_candidates() -> list[Path]:
    """Return the default workbook search paths in priority order."""
    return [project_path(str(path)) for path in DEFAULT_WORKBOOK_RELATIVE_PATHS]


def find_default_workbook() -> Path | None:
    """Find the first default workbook candidate that exists."""
    for path in default_workbook_candidates():
        if path.is_file():
            return path
    return None


def default_output_dir() -> Path:
    """Return the default generated extraction output directory."""
    return project_path("data/normalized/legacy-workbook")


def resolve_workbook_path(path: Path | None) -> Path:
    """Resolve a user-supplied workbook path or default search path."""
    if path is not None:
        resolved = path if path.is_absolute() else project_path(str(path))
        if resolved.is_file():
            return resolved
        raise FileNotFoundError(f"Legacy workbook not found: {resolved}")

    found = find_default_workbook()
    if found is not None:
        return found

    searched = ", ".join(str(candidate) for candidate in default_workbook_candidates())
    raise FileNotFoundError(f"Legacy workbook not found. Searched: {searched}")
