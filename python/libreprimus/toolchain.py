"""Small, non-invasive toolchain report helpers."""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


COMMANDS: tuple[str, ...] = ("git", "cmake", "ninja", "py", "python", "cl", "nvcc", "nvidia-smi")


@dataclass(frozen=True)
class ToolStatus:
    name: str
    present: bool
    path: str | None
    version: str | None


def _which(command: str) -> str | None:
    path = shutil.which(command)
    if path is not None:
        return path

    if command == "ninja":
        winget_root = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Packages"
        if winget_root.is_dir():
            for candidate in winget_root.rglob("ninja.exe"):
                return str(candidate)

    return None


def _version_for(command: str, executable: str | None) -> str | None:
    if executable is None:
        return None

    args = [executable, "--version"]
    if command == "py":
        args = [executable, "-0p"]

    try:
        completed = subprocess.run(
            args,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None

    text = (completed.stdout or completed.stderr).strip()
    if not text:
        return None
    return text.splitlines()[0]


def collect_toolchain() -> dict[str, ToolStatus | str | None]:
    """Collect a concise toolchain report without printing the full environment."""
    report: dict[str, ToolStatus | str | None] = {}
    for command in COMMANDS:
        path = _which(command)
        report[command] = ToolStatus(
            name=command,
            present=path is not None,
            path=path,
            version=_version_for(command, path),
        )

    report["CUDA_PATH"] = os.environ.get("CUDA_PATH")
    return report
