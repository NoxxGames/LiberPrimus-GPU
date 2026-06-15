"""Project-local Stop hook for stale current-stage claims."""

from __future__ import annotations

from pathlib import Path

from hook_common import drain_stdin, python_for_repo, repo_root_from, run_hook_command, strict_mode


def main() -> int:
    drain_stdin()
    root = repo_root_from(Path(__file__))
    report = root / "experiments/results/doc-drift/stage6b-stop-hook-audit.json"
    command = [
        str(python_for_repo(root)),
        "-m",
        "libreprimus.cli",
        "consistency",
        "audit-stale-current-claims",
        "--strict",
        "--out",
        str(report),
    ]
    if not strict_mode():
        command.append("--report-only")
    return run_hook_command(command, root=root, report_path=report, timeout=110)


if __name__ == "__main__":
    raise SystemExit(main())
