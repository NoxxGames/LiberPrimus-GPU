"""Build Stage 5T benchmark-readiness planning records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_solved_family_readiness.export import write_record_set, write_report
from libreprimus.cuda_solved_family_readiness.models import BENCHMARK_READINESS_PATH, BENCHMARK_READINESS_REPORT_JSON, COMMON_FLAGS, OUTPUT_DIR


def build_benchmark_readiness(
    *,
    benchmark_readiness_out: Path = BENCHMARK_READINESS_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records = [
        _record("cpu_reference_baseline_plan", "planning_only", True, "CPU baseline plan can be specified without running timings."),
        _record("cuda_microbenchmark_plan", "blocked_pending_stage5u_abi", True, "CUDA benchmark design needs unified ABI first; execution remains blocked."),
        _record("end_to_end_speedup_claim", "blocked_not_evidence", False, "End-to-end speedup claims are not allowed in readiness records."),
    ]
    write_record_set(benchmark_readiness_out, records)
    write_report(out_dir, BENCHMARK_READINESS_REPORT_JSON, {"records": records})
    return records


def _record(record_id: str, status: str, planning_allowed: bool, rationale: str) -> dict[str, Any]:
    return {
        "record_type": "cuda_benchmark_readiness_record",
        "benchmark_readiness_id": f"stage5t-benchmark-{record_id}",
        "benchmark_surface_id": record_id,
        "readiness_status": status,
        "benchmark_planning_allowed": planning_allowed,
        "benchmark_execution_allowed": False,
        "performance_claim_allowed": False,
        "speedup_claim_allowed": False,
        "rationale": rationale,
        **COMMON_FLAGS,
    }
