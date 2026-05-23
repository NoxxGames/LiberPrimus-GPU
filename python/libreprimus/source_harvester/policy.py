"""Output-root and policy helpers for source harvesting."""

from __future__ import annotations

from pathlib import Path

from libreprimus.paths import repo_root

ALLOWED_REPO_OUTPUT_ROOTS = (
    Path("experiments/results/source-harvester"),
    Path("source-harvester-output"),
    Path("harvest-output"),
    Path("research-inputs"),
)


def is_inside_repo(path: Path) -> bool:
    """Return whether a path resolves inside the repository."""

    try:
        path.resolve().relative_to(repo_root())
        return True
    except ValueError:
        return False


def repo_relative(path: Path) -> Path | None:
    """Return a repo-relative path when possible."""

    try:
        return path.resolve().relative_to(repo_root())
    except ValueError:
        return None


def is_allowed_output_root(path: Path) -> bool:
    """Return true for external paths or explicitly ignored local harvester roots."""

    relative = repo_relative(path)
    if relative is None:
        return True
    return any(relative == allowed or allowed in relative.parents for allowed in ALLOWED_REPO_OUTPUT_ROOTS)


def require_safe_output_root(path: Path) -> None:
    """Reject committed repository paths as raw output roots."""

    if not is_allowed_output_root(path):
        raise ValueError(
            "output root is inside the repository but is not an ignored source-harvester output root"
        )
