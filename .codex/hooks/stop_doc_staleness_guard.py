"""Project-local Stop hook for stale current-stage claims."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def main() -> int:
    root = _repo_root()
    report = root / "experiments/results/doc-drift/stage5eg-stop-hook-audit.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    python = _python(root)
    command = [
        str(python),
        "-m",
        "libreprimus.cli",
        "consistency",
        "audit-stale-current-claims",
        "--strict",
        "--out",
        str(report),
    ]
    result = subprocess.run(command, cwd=root, text=True, capture_output=True, timeout=110)
    print(result.stdout.strip())
    if result.returncode != 0:
        print(result.stderr.strip(), file=sys.stderr)
        print(f"Stale current-stage claims remain. Fix them before closeout. Report: {report}", file=sys.stderr)
    return result.returncode


def _repo_root() -> Path:
    path = Path.cwd().resolve()
    for candidate in (path, *path.parents):
        if (candidate / ".git").exists():
            return candidate
    return path


def _python(root: Path) -> Path:
    windows = root / ".venv/Scripts/python.exe"
    posix = root / ".venv/bin/python"
    if windows.exists():
        return windows
    if posix.exists():
        return posix
    return Path(sys.executable)


if __name__ == "__main__":
    raise SystemExit(main())
