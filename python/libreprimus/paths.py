"""Path helpers for the Stage 0A repository scaffold."""

from pathlib import Path


def package_root() -> Path:
    """Return the installed package directory."""
    return Path(__file__).resolve().parent


def repo_root() -> Path:
    """Return the repository root for editable/source-tree usage."""
    return package_root().parents[1]


def project_path(*parts: str) -> Path:
    """Return a path under the repository root."""
    return repo_root().joinpath(*parts)
