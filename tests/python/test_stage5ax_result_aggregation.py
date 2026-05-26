from __future__ import annotations

from pathlib import Path

from libreprimus.parallel_validation.models import CommandResult
from libreprimus.parallel_validation.results import aggregate_results


def test_aggregate_exit_code_zero_when_all_commands_pass(tmp_path: Path) -> None:
    result = CommandResult("ok", "ok", 0, 0.1, "ok.out", "ok.err")
    pytest_result = {
        "pytest_mode_requested": "serial",
        "pytest_mode_used": "serial",
        "pytest_xdist_available": False,
        "pytest_shard_fallback_used": False,
        "passed": True,
        "failure_count": 0,
        "duration_seconds": 0.1,
    }
    summary = aggregate_results(
        [result],
        pytest_result,
        workers_requested=1,
        workers_used=1,
        pytest_workers_requested=1,
        pytest_workers_used=1,
        duration_seconds=0.2,
        results_dir=tmp_path,
    )
    assert summary["aggregate_exit_code"] == 0
    assert summary["commands_failed"] == 0
    assert summary["validation_timing_recorded"] is True
