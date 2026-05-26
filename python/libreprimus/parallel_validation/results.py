"""Result aggregation and export helpers for Stage 5AX."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

from .models import CommandResult


def write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def read_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


def aggregate_results(
    command_results: list[CommandResult],
    pytest_result: dict[str, Any],
    *,
    workers_requested: int,
    workers_used: int,
    pytest_workers_requested: int,
    pytest_workers_used: int,
    duration_seconds: float,
    results_dir: Path,
) -> dict[str, Any]:
    failures = [result for result in command_results if not result.passed]
    pytest_failures = pytest_result.get("failure_count", 0)
    failed_command_ids = [result.command_id for result in failures]
    if pytest_failures:
        failed_command_ids.append("pytest")
    end_time = datetime.now(UTC)
    start_time = end_time - timedelta(seconds=duration_seconds)
    return {
        "record_type": "stage5ax_parallel_validation_run_summary",
        "schema": "schemas/ci/parallel-validation-run-summary-v0.schema.json",
        "stage_id": "stage-5ax",
        "status": "passed" if not failed_command_ids else "failed",
        "start_time_utc": start_time.isoformat().replace("+00:00", "Z"),
        "end_time_utc": end_time.isoformat().replace("+00:00", "Z"),
        "workers_requested": workers_requested,
        "workers_used": workers_used,
        "pytest_workers_requested": pytest_workers_requested,
        "pytest_workers_used": pytest_workers_used,
        "pytest_mode_requested": pytest_result["pytest_mode_requested"],
        "pytest_mode_used": pytest_result["pytest_mode_used"],
        "pytest_xdist_available": pytest_result["pytest_xdist_available"],
        "pytest_shard_fallback_used": pytest_result["pytest_shard_fallback_used"],
        "parallel_command_count": len(command_results),
        "serial_command_count": 0,
        "commands_started": len(command_results) + 1,
        "commands_succeeded": len(command_results) - len(failures) + int(pytest_result["passed"]),
        "commands_failed": len(failed_command_ids),
        "failed_command_count": len(failed_command_ids),
        "failed_command_ids": failed_command_ids,
        "aggregate_exit_code": 0 if not failed_command_ids else 1,
        "logs_root": str((results_dir / "logs").as_posix()),
        "timing_records_path": str((results_dir / "timings.jsonl").as_posix()),
        "failure_records_path": str((results_dir / "failures.jsonl").as_posix()),
        "success_count": len(command_results) - len(failures) + int(pytest_result["passed"]),
        "failure_count": len(failed_command_ids),
        "pytest_passed": pytest_result["passed"],
        "ruff_passed": any(
            result.command_id == "ruff-check" and result.passed for result in command_results
        ),
        "serial_final_confirmation_recorded": True,
        "generated_validation_outputs_committed": False,
        "validation_timing_recorded": True,
        "benchmark_performed": False,
        "cryptanalytic_benchmark_performed": False,
        "duration_seconds": round(duration_seconds, 6),
        "command_results": [result.to_record() for result in command_results],
        "pytest_result": pytest_result,
    }


def export_run_outputs(
    results_dir: Path,
    run_summary: dict[str, Any],
    command_results: list[CommandResult],
) -> None:
    results_dir.mkdir(parents=True, exist_ok=True)
    write_json(results_dir / "run-summary.json", run_summary)
    write_jsonl(results_dir / "commands.jsonl", [result.to_record() for result in command_results])
    failures = [result.to_record() for result in command_results if not result.passed]
    if not run_summary.get("pytest_passed", False):
        failures.append({"command_id": "pytest", "passed": False})
    write_jsonl(results_dir / "failures.jsonl", failures)
    timing_records = [
        {
            "command_id": result.command_id,
            "duration_seconds": round(result.duration_seconds, 6),
            "validation_timing_recorded": True,
            "benchmark_performed": False,
            "cryptanalytic_benchmark_performed": False,
        }
        for result in command_results
    ]
    timing_records.append(
        {
            "command_id": "pytest",
            "duration_seconds": run_summary["pytest_result"]["duration_seconds"],
            "validation_timing_recorded": True,
            "benchmark_performed": False,
            "cryptanalytic_benchmark_performed": False,
        }
    )
    write_jsonl(results_dir / "timings.jsonl", timing_records)
    write_json(results_dir / "pytest-shards.json", run_summary["pytest_result"])
