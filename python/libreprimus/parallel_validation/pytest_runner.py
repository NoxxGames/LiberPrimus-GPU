"""Pytest xdist detection and deterministic sharded fallback."""

from __future__ import annotations

import importlib.util
import math
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any


def pytest_xdist_available() -> bool:
    """Return true when pytest-xdist is importable."""

    return importlib.util.find_spec("xdist") is not None


def discover_test_files(test_root: Path) -> list[Path]:
    """Discover pytest files in deterministic order."""

    return sorted(path for path in test_root.rglob("test_*.py") if path.is_file())


def build_shards(test_files: list[Path], worker_count: int) -> list[list[Path]]:
    """Partition tests deterministically across up to worker_count shards."""

    if worker_count < 1:
        raise ValueError("worker_count must be positive")
    if not test_files:
        return []
    shard_count = min(worker_count, len(test_files))
    shards: list[list[Path]] = [[] for _ in range(shard_count)]
    for index, path in enumerate(test_files):
        shards[index % shard_count].append(path)
    return shards


def shard_plan_record(test_root: Path, worker_count: int) -> dict[str, Any]:
    """Build a committed metadata shard plan without executing pytest."""

    files = discover_test_files(test_root)
    shards = build_shards(files, worker_count)
    return {
        "record_type": "stage5ax_pytest_shard_plan",
        "schema": "schemas/ci/pytest-shard-plan-v0.schema.json",
        "stage_id": "stage-5ax",
        "test_root": str(test_root.as_posix()),
        "requested_workers": worker_count,
        "shard_count": len(shards),
        "test_file_count": len(files),
        "all_tests_covered_once": True,
        "shards": [
            {
                "shard_id": f"pytest-shard-{index + 1:02d}",
                "test_file_count": len(shard),
                "test_files": [str(path.as_posix()) for path in shard],
            }
            for index, shard in enumerate(shards)
        ],
    }


def select_pytest_mode(requested_mode: str) -> tuple[str, bool, bool]:
    """Resolve auto/xdist/shard/serial into the mode used."""

    xdist = pytest_xdist_available()
    mode = requested_mode
    if requested_mode == "auto":
        mode = "xdist" if xdist else "shard"
    if mode == "xdist" and not xdist:
        mode = "shard"
    return mode, xdist, mode == "shard"


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _run_pytest_shard(
    shard_id: str,
    files: list[Path],
    repo_root: Path,
    log_dir: Path,
    timeout_seconds: int,
) -> dict[str, Any]:
    started = time.perf_counter()
    cmd = [sys.executable, "-m", "pytest", "-q", *[str(path.as_posix()) for path in files]]
    try:
        completed = subprocess.run(
            cmd,
            cwd=repo_root,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
        returncode = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        returncode = 124
        stdout = exc.stdout or ""
        stderr = (exc.stderr or "") + f"\nTimed out after {timeout_seconds} seconds.\n"
        timed_out = True
    duration = time.perf_counter() - started
    stdout_log = log_dir / f"{shard_id}.stdout.log"
    stderr_log = log_dir / f"{shard_id}.stderr.log"
    _write_text(stdout_log, stdout)
    _write_text(stderr_log, stderr)
    return {
        "command_id": shard_id,
        "display_name": shard_id,
        "returncode": returncode,
        "duration_seconds": round(duration, 6),
        "stdout_log": str(stdout_log.as_posix()),
        "stderr_log": str(stderr_log.as_posix()),
        "timed_out": timed_out,
        "passed": returncode == 0 and not timed_out,
        "test_file_count": len(files),
    }


def run_pytest(
    *,
    repo_root: Path,
    test_root: Path,
    results_dir: Path,
    requested_mode: str,
    worker_count: int,
    timeout_seconds: int = 1200,
) -> dict[str, Any]:
    """Run pytest using xdist, shard fallback, or serial mode."""

    mode, xdist, shard_fallback = select_pytest_mode(requested_mode)
    started = time.perf_counter()
    log_dir = results_dir / "logs" / "pytest"
    log_dir.mkdir(parents=True, exist_ok=True)

    if mode == "serial":
        shard_fallback = False
        result = _run_pytest_shard("pytest-serial", [test_root], repo_root, log_dir, timeout_seconds)
        shard_results = [result]
    elif mode == "xdist":
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            str(test_root.as_posix()),
            "-n",
            str(worker_count),
        ]
        proc_started = time.perf_counter()
        completed = subprocess.run(
            cmd,
            cwd=repo_root,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
        stdout_log = log_dir / "pytest-xdist.stdout.log"
        stderr_log = log_dir / "pytest-xdist.stderr.log"
        _write_text(stdout_log, completed.stdout)
        _write_text(stderr_log, completed.stderr)
        shard_results = [
            {
                "command_id": "pytest-xdist",
                "display_name": "pytest xdist",
                "returncode": completed.returncode,
                "duration_seconds": round(time.perf_counter() - proc_started, 6),
                "stdout_log": str(stdout_log.as_posix()),
                "stderr_log": str(stderr_log.as_posix()),
                "timed_out": False,
                "passed": completed.returncode == 0,
                "test_file_count": len(discover_test_files(test_root)),
            }
        ]
    else:
        files = discover_test_files(test_root)
        shards = build_shards(files, worker_count)
        log_workers = min(worker_count, len(shards)) if shards else 1
        with ThreadPoolExecutor(max_workers=max(1, log_workers)) as executor:
            futures = {
                executor.submit(
                    _run_pytest_shard,
                    f"pytest-shard-{index + 1:02d}",
                    shard,
                    repo_root,
                    log_dir,
                    timeout_seconds,
                ): index
                for index, shard in enumerate(shards)
            }
            shard_results = [future.result() for future in as_completed(futures)]
        shard_results = sorted(shard_results, key=lambda item: item["command_id"])

    failures = [item for item in shard_results if not item["passed"]]
    duration = time.perf_counter() - started
    result = {
        "record_type": "stage5ax_pytest_run_summary",
        "pytest_mode_requested": requested_mode,
        "pytest_mode_used": mode,
        "pytest_workers_requested": worker_count,
        "pytest_workers_used": worker_count,
        "pytest_xdist_available": xdist,
        "pytest_shard_fallback_used": shard_fallback,
        "pytest_shard_count": len(shard_results) if mode == "shard" else 0,
        "test_file_count": len(discover_test_files(test_root)),
        "failure_count": len(failures),
        "success_count": len(shard_results) - len(failures),
        "passed": not failures,
        "duration_seconds": round(duration, 6),
        "shard_results": shard_results,
    }
    return result


def recommended_pytest_workers(requested: int, max_workers: int) -> int:
    """Cap pytest workers for file sharding."""

    cpu_count = os.cpu_count() or 1
    return max(1, min(requested, max_workers, cpu_count))


def estimated_files_per_worker(file_count: int, workers: int) -> int:
    """Small helper used by tests and summaries."""

    return int(math.ceil(file_count / max(1, workers)))
