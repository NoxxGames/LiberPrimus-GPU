"""Explicit operator-action file and URL opening helpers."""

from __future__ import annotations

import os
import subprocess
import sys
import webbrowser
from pathlib import Path

from .path_aliases import resolve_with_aliases


def open_file(path: Path) -> None:
    path = _resolve_path(path)
    if sys.platform.startswith("win"):
        os.startfile(path)  # type: ignore[attr-defined]
    elif sys.platform == "darwin":
        subprocess.run(["open", str(path)], check=False)
    else:
        subprocess.run(["xdg-open", str(path)], check=False)


def open_file_location(path: Path) -> None:
    path = _resolve_path(path)
    if sys.platform.startswith("win"):
        subprocess.run(["explorer", f"/select,{path}"], check=False)
    elif sys.platform == "darwin":
        subprocess.run(["open", "-R", str(path)], check=False)
    else:
        subprocess.run(["xdg-open", str(path.parent)], check=False)


def open_url(url: str) -> None:
    webbrowser.open(url)


def _resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else resolve_with_aliases(path.as_posix())
