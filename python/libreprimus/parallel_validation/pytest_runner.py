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

DEFAULT_WORKERS = 10
DEFAULT_MAX_WORKERS = 10

SERIAL_ISOLATED_TEST_FILES = frozenset(
    {
        Path("tests/python/test_stage5cu_cli.py"),
        Path("tests/python/test_stage5cu_options_nonselection.py"),
    }
)

SLOW_TEST_FILE_WEIGHTS = {
    "test_stage5dy_cli.py": 4,
    "test_stage5dz_cli.py": 4,
    "test_stage5ea_cli.py": 4,
    "test_stage5ea_source_browser_performance.py": 3,
    "test_stage5eb_cli.py": 4,
    "test_stage5eb_source_browser_cache_reuse.py": 3,
    "test_stage5eb_generic_stage_wrapper.py": 2,
}


def pytest_xdist_available() -> bool:
    """Return true when pytest-xdist is importable."""

    return importlib.util.find_spec("xdist") is not None


def discover_test_files(test_root: Path) -> list[Path]:
    """Discover pytest files in deterministic order."""

    return sorted(path for path in test_root.rglob("test_*.py") if path.is_file())


def _repo_relative(path: Path) -> Path:
    return Path(path.as_posix())


def serial_isolated_test_files(test_files: list[Path]) -> list[Path]:
    """Return files that must run outside parallel shards."""

    return [path for path in test_files if _repo_relative(path) in SERIAL_ISOLATED_TEST_FILES]


def parallel_test_files(test_files: list[Path]) -> list[Path]:
    """Return files eligible for parallel pytest shards."""

    return [path for path in test_files if _repo_relative(path) not in SERIAL_ISOLATED_TEST_FILES]


def pytest_file_weight(path: Path) -> int:
    """Return a deterministic relative shard weight for known slow tests."""

    return max(1, SLOW_TEST_FILE_WEIGHTS.get(path.name, 1))


def build_shards(test_files: list[Path], worker_count: int) -> list[list[Path]]:
    """Partition tests deterministically across up to worker_count shards."""

    if worker_count < 1:
        raise ValueError("worker_count must be positive")
    if not test_files:
        return []
    shard_count = min(worker_count, len(test_files))
    shards: list[list[Path]] = [[] for _ in range(shard_count)]
    shard_weights = [0 for _ in range(shard_count)]
    weighted_files = sorted(test_files, key=lambda path: (-pytest_file_weight(path), path.as_posix()))
    for path in weighted_files:
        shard_index = min(range(shard_count), key=lambda index: (shard_weights[index], index))
        shards[shard_index].append(path)
        shard_weights[shard_index] += pytest_file_weight(path)
    for shard in shards:
        shard.sort(key=lambda path: path.as_posix())
    return shards


def shard_plan_record(test_root: Path, worker_count: int) -> dict[str, Any]:
    """Build a committed metadata shard plan without executing pytest."""

    files = discover_test_files(test_root)
    isolated = serial_isolated_test_files(files)
    parallel_files = parallel_test_files(files)
    shards = build_shards(parallel_files, worker_count)
    return {
        "record_type": "stage5ax_pytest_shard_plan",
        "schema": "schemas/ci/pytest-shard-plan-v0.schema.json",
        "stage_id": "stage-5ax",
        "test_root": str(test_root.as_posix()),
        "requested_workers": worker_count,
        "shard_count": len(shards),
        "test_file_count": len(files),
        "parallel_test_file_count": len(parallel_files),
        "serial_isolated_test_file_count": len(isolated),
        "serial_isolated_test_files": [str(path.as_posix()) for path in isolated],
        "duration_aware_balancing": True,
        "known_serial_isolated_files_recorded": True,
        "slow_test_weights": dict(sorted(SLOW_TEST_FILE_WEIGHTS.items())),
        "all_tests_covered_once": True,
        "shards": [
            {
                "shard_id": f"pytest-shard-{index + 1:02d}",
                "test_file_count": len(shard),
                "estimated_weight": sum(pytest_file_weight(path) for path in shard),
                "weight": sum(pytest_file_weight(path) for path in shard),
                "test_files": [str(path.as_posix()) for path in shard],
                "rerun_command": _pytest_rerun_command(shard),
            }
            for index, shard in enumerate(shards)
        ],
    }


def select_pytest_mode(requested_mode: str) -> tuple[str, bool, bool]:
    """Resolve auto/xdist/shard/serial into the mode used."""

    xdist = pytest_xdist_available()
    mode = requested_mode
    if requested_mode == "auto":
        # Several stage-builder tests regenerate shared YAML/schema files. On
        # Windows, xdist can make readers observe transient file-access
        # contention even though writes are atomic. File-level shards keep the
        # local validation path parallel while avoiding that race.
        if sys.platform.startswith("win"):
            mode = "shard"
        else:
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
        "test_files": [str(path.as_posix()) for path in files],
        "rerun_command": _pytest_rerun_command(files),
    }


def run_pytest(
    *,
    repo_root: Path,
    test_root: Path,
    results_dir: Path,
    requested_mode: str,
    worker_count: int,
    timeout_seconds: int = 3600,
) -> dict[str, Any]:
    """Run pytest using xdist, shard fallback, or serial mode."""

    mode, xdist, shard_fallback = select_pytest_mode(requested_mode)
    files = discover_test_files(test_root)
    isolated_files = serial_isolated_test_files(files)
    if mode == "xdist" and isolated_files:
        mode = "shard"
        shard_fallback = True
    started = time.perf_counter()
    log_dir = results_dir / "logs" / "pytest"
    log_dir.mkdir(parents=True, exist_ok=True)
    parallel_shard_count = 0

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
                "test_file_count": len(files),
                "test_files": [str(path.as_posix()) for path in files],
                "rerun_command": f"{sys.executable} -m pytest -q {test_root.as_posix()} -n {worker_count}",
            }
        ]
    else:
        parallel_files = parallel_test_files(files)
        shards = build_shards(parallel_files, worker_count)
        parallel_shard_count = len(shards)
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
        if isolated_files:
            shard_results.append(
                _run_pytest_shard(
                    "pytest-serial-isolated",
                    isolated_files,
                    repo_root,
                    log_dir,
                    timeout_seconds,
                )
            )

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
        "pytest_shard_count": parallel_shard_count if mode == "shard" else 0,
        "pytest_serial_isolated_count": len(isolated_files) if mode == "shard" else 0,
        "pytest_serial_isolated_files": [
            str(path.as_posix()) for path in isolated_files
        ]
        if mode == "shard"
        else [],
        "test_file_count": len(files),
        "failure_count": len(failures),
        "failure_rerun_commands": [str(item["rerun_command"]) for item in failures if item.get("rerun_command")],
        "rerun_guidance": _rerun_guidance(failures),
        "success_count": len(shard_results) - len(failures),
        "passed": not failures,
        "duration_seconds": round(duration, 6),
        "shard_results": shard_results,
    }
    return result


def _pytest_rerun_command(files: list[Path]) -> str:
    if not files:
        return f"{sys.executable} -m pytest -q"
    return " ".join([sys.executable, "-m", "pytest", "-q", *[path.as_posix() for path in files]])


def _rerun_guidance(failures: list[dict[str, Any]]) -> str:
    if not failures:
        return "No pytest shard failures."
    commands = [str(item["rerun_command"]) for item in failures if item.get("rerun_command")]
    return (
        "Rerun failing pytest shard before rerunning full parallel validation: "
        + " && ".join(commands)
    )


def recommended_pytest_workers(requested: int, max_workers: int) -> int:
    """Cap pytest workers for file sharding."""

    cpu_count = os.cpu_count() or 1
    return max(1, min(requested, max_workers, cpu_count))


def estimated_files_per_worker(file_count: int, workers: int) -> int:
    """Small helper used by tests and summaries."""

    return int(math.ceil(file_count / max(1, workers)))
