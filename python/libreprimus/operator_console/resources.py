"""Resource helpers for Operator Console data roots."""

from __future__ import annotations

from pathlib import Path

import yaml

from .settings import (
    CACHE_ROOT,
    DEFAULT_COLUMN_PROFILE,
    DEFAULT_COLUMNS,
    DEFAULT_PATH_ALIASES,
    REQUIRED_DATA_DIRS,
    THUMBNAIL_CACHE_DIR,
)


def ensure_operator_console_dirs() -> None:
    """Create committed config/scaffold directories and ignored cache directories."""
    for path in REQUIRED_DATA_DIRS:
        path.mkdir(parents=True, exist_ok=True)
        keep = path / ".gitkeep"
        if not keep.exists():
            keep.write_text("", encoding="utf-8")
    CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    THUMBNAIL_CACHE_DIR.mkdir(parents=True, exist_ok=True)


def ensure_default_configs() -> None:
    """Write portable default config files if they do not already exist."""
    ensure_operator_console_dirs()
    if not DEFAULT_PATH_ALIASES.exists():
        DEFAULT_PATH_ALIASES.write_text(
            yaml.safe_dump(
                {
                    "record_type": "source_browser_path_aliases",
                    "schema": "schemas/operator-console/source-browser-path-aliases-v0.schema.json",
                    "profile_id": "default",
                    "path_aliases": [
                        {"from": "third_party", "to": "third_party"},
                        {"from": "data", "to": "data"},
                    ],
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
    if not DEFAULT_COLUMN_PROFILE.exists():
        DEFAULT_COLUMN_PROFILE.write_text(
            yaml.safe_dump(
                {
                    "record_type": "source_browser_column_profile",
                    "schema": "schemas/operator-console/source-browser-column-profile-v0.schema.json",
                    "profile_id": "default",
                    "columns": [
                        {"key": key, "label": label, "width": width}
                        for key, label, width in DEFAULT_COLUMNS
                    ],
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()
