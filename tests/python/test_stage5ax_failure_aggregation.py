from __future__ import annotations

from pathlib import Path

from libreprimus.parallel_validation.models import CommandResult
from libreprimus.parallel_validation.results import aggregate_results


def test_failure_aggregation_preserves_failed_command_ids(tmp_path: Path) -> None:
    failed = CommandResult("bad", "bad", 1, 0.1, "bad.out", "bad.err")
    pytest_result = {
        "pytest_mode_requested": "serial",
        "pytest_mode_used": "serial",
        "pytest_xdist_available": False,
        "pytest_shard_fallback_used": False,
        "passed": False,
        "failure_count": 1,
        "duration_seconds": 0.1,
    }
    summary = aggregate_results(
        [failed],
        pytest_result,
        workers_requested=1,
        workers_used=1,
        pytest_workers_requested=1,
        pytest_workers_used=1,
        duration_seconds=0.2,
        results_dir=tmp_path,
    )
    assert summary["aggregate_exit_code"] == 1
    assert summary["failed_command_ids"] == ["bad", "pytest"]
