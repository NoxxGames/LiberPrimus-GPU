"""Parallel command scheduler for Stage 5AX."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Iterable

from .models import PARALLEL_SAFE_CLASSES, CommandResult, ValidationCommand
from .subprocess_runner import run_command


def cap_workers(requested: int | None, policy_max: int, cpu_count: int | None) -> int:
    """Cap a requested worker count by policy and CPU availability."""

    base = requested or policy_max
    cpu_cap = cpu_count or 1
    return max(1, min(base, policy_max, cpu_cap))


def assert_parallel_safe(command: ValidationCommand) -> None:
    """Raise if a command is not explicitly parallel-safe."""

    if command.parallel_class not in PARALLEL_SAFE_CLASSES or command.requires_serial:
        raise ValueError(f"Command {command.command_id} is not parallel-safe")
    if command.uses_git_mutation or command.uses_github_mutation:
        raise ValueError(f"Command {command.command_id} mutates git or GitHub")


def run_parallel_commands(
    commands: Iterable[ValidationCommand],
    *,
    repo_root: Path,
    results_dir: Path,
    workers: int,
) -> list[CommandResult]:
    """Run parallel-safe commands concurrently and return deterministic results."""

    command_list = sorted(commands, key=lambda item: item.command_id)
    for command in command_list:
        assert_parallel_safe(command)

    log_dir = results_dir / "logs" / "commands"
    results: list[CommandResult] = []
    with ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
        futures = {
            executor.submit(run_command, command, repo_root=repo_root, log_dir=log_dir): command
            for command in command_list
        }
        for future in as_completed(futures):
            results.append(future.result())
    return sorted(results, key=lambda item: item.command_id)
