"""Shared helpers for project-local Codex hooks."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

STRICT_ENV_VAR = "LIBERPRIMUS_CODEX_HOOK_STRICT"


def strict_mode() -> bool:
    return os.environ.get(STRICT_ENV_VAR) == "1"


def repo_root_from(start: Path | None = None) -> Path:
    candidates: list[Path] = []
    if start is not None:
        candidates.append(start.resolve())
    candidates.append(Path(__file__).resolve())
    candidates.append(Path.cwd().resolve())
    for base in candidates:
        for candidate in (base, *base.parents):
            if (candidate / ".git").exists() and (candidate / "python/libreprimus").exists():
                return candidate
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return Path(result.stdout.strip()).resolve()
    except Exception:
        pass
    return Path.cwd().resolve()


def python_for_repo(root: Path) -> Path:
    windows = root / ".venv" / "Scripts" / "python.exe"
    posix = root / ".venv" / "bin" / "python"
    if windows.exists():
        return windows
    if posix.exists():
        return posix
    return Path(sys.executable)


def env_for_repo(root: Path) -> dict[str, str]:
    env = os.environ.copy()
    python_dir = str(root / "python")
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = python_dir if not existing else f"{python_dir}{os.pathsep}{existing}"
    return env


def drain_stdin() -> None:
    try:
        if not sys.stdin.closed:
            sys.stdin.read()
    except Exception:
        pass


def write_report(path: Path, payload: dict[str, Any]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"LiberPrimus hook warning: could not write report {path}: {exc}", file=sys.stderr)


def run_hook_command(command: list[str], *, root: Path, report_path: Path, timeout: int) -> int:
    strict = strict_mode()
    payload: dict[str, Any] = {
        "report_kind": "codex_stop_doc_staleness_guard"
        if "stop" in report_path.name
        else "codex_hook_report",
        "report_producer": ".codex/hooks/stop_doc_staleness_guard.py"
        if "stop" in report_path.name
        else ".codex/hooks",
        "authoritative_automation_report": False,
        "may_be_used_as_latest_automation_report": False,
        "strict_mode": strict,
        "scanner_command_failed": False,
        "hook_environment_failure": False,
        "hook_default_mode": "strict" if strict else "report_only",
        "report_path": report_path.as_posix(),
    }
    try:
        result = subprocess.run(
            command,
            cwd=root,
            env=env_for_repo(root),
            text=True,
            capture_output=True,
            timeout=timeout,
        )
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        if stdout:
            print(stdout)
        if stderr:
            print(stderr, file=sys.stderr)
        payload.update(
            {
                "command": command,
                "scanner_return_code": result.returncode,
                "scanner_command_failed": result.returncode != 0,
                "stdout": stdout,
                "stderr": stderr,
                "stale_current_strict_errors_found": _count(stdout, "stale_current_error_count"),
                "stale_current_warnings_found": _count(stdout, "stale_current_warning_count"),
            }
        )
        exit_code = result.returncode if strict else 0
    except Exception as exc:
        payload.update(
            {
                "command": command,
                "scanner_command_failed": True,
                "hook_environment_failure": True,
                "exception": repr(exc),
                "stale_current_strict_errors_found": None,
                "stale_current_warnings_found": None,
            }
        )
        print(f"LiberPrimus hook warning: {exc}", file=sys.stderr)
        exit_code = 1 if strict else 0
    payload["exit_code"] = exit_code
    write_report(report_path, payload)
    return exit_code


def _count(text: str, key: str) -> int | None:
    prefix = f"{key}="
    for line in text.splitlines():
        if line.startswith(prefix):
            try:
                return int(line.removeprefix(prefix).strip())
            except ValueError:
                return None
    return None
