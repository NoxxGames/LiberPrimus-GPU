"""Benchmark environment diagnostics for Stage 4Q."""

from __future__ import annotations

from datetime import UTC, datetime
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import resolve_repo_path, write_json
from libreprimus.benchmark_planning.models import CPU_ONLY_POLICY, ENVIRONMENT_JSON, STAGE4Q_OUTPUT_DIR


def build_environment_record(*, out_dir: Path = STAGE4Q_OUTPUT_DIR) -> dict[str, Any]:
    """Write a raw-data-free benchmark environment record."""

    record = {
        "record_type": "benchmark_environment_record",
        "benchmark_scope": "environment_record",
        "benchmark_status": "planned",
        "environment_id": "stage4q-local-cpu-environment",
        "recorded_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "git_commit": _git_text("rev-parse", "HEAD"),
        "git_branch": _git_text("branch", "--show-current"),
        "absolute_paths_committed": False,
        **CPU_ONLY_POLICY,
    }
    resolved_out = resolve_repo_path(out_dir)
    write_json(resolved_out / ENVIRONMENT_JSON, record)
    return record


def _git_text(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=resolve_repo_path(Path(".")),
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        return "unknown"
    return result.stdout.strip()
