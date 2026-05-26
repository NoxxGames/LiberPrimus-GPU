"""Subprocess execution helpers for parallel validation."""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Mapping

from .models import CommandResult, ValidationCommand


def resolve_command(command: list[str]) -> list[str]:
    """Resolve portable placeholders in a command vector."""

    resolved: list[str] = []
    for part in command:
        if part == "{python}":
            resolved.append(sys.executable)
        elif part == "{powershell}":
            resolved.append(os.environ.get("POWERSHELL_EXE", "powershell"))
        else:
            resolved.append(part)
    return resolved


def _safe_log_name(command_id: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in command_id)


def run_command(
    command: ValidationCommand,
    *,
    repo_root: Path,
    log_dir: Path,
    extra_env: Mapping[str, str] | None = None,
) -> CommandResult:
    """Run one classified command and write separated stdout/stderr logs."""

    log_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(command.env)
    if extra_env:
        env.update(extra_env)

    cwd = repo_root / command.working_directory
    stdout_log = log_dir / f"{_safe_log_name(command.command_id)}.stdout.log"
    stderr_log = log_dir / f"{_safe_log_name(command.command_id)}.stderr.log"
    started = time.perf_counter()
    timed_out = False
    try:
        completed = subprocess.run(
            resolve_command(command.command),
            cwd=cwd,
            env=env,
            text=True,
            capture_output=True,
            timeout=command.timeout_seconds,
            check=False,
        )
        returncode = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        returncode = 124
        stdout = exc.stdout or ""
        stderr = (exc.stderr or "") + f"\nTimed out after {command.timeout_seconds} seconds.\n"
    duration = time.perf_counter() - started
    stdout_log.write_text(stdout, encoding="utf-8")
    stderr_log.write_text(stderr, encoding="utf-8")
    return CommandResult(
        command_id=command.command_id,
        display_name=command.display_name,
        returncode=returncode,
        duration_seconds=duration,
        stdout_log=str(stdout_log.as_posix()),
        stderr_log=str(stderr_log.as_posix()),
        timed_out=timed_out,
    )
