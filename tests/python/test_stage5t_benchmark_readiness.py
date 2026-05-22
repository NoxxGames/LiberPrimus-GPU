from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5t_benchmark_readiness_is_planning_only() -> None:
    records = yaml.safe_load(Path("data/cuda/stage5t-cuda-benchmark-readiness.yaml").read_text(encoding="utf-8"))[
        "records"
    ]
    by_surface = {record["benchmark_surface_id"]: record for record in records}
    assert by_surface["cpu_reference_baseline_plan"]["benchmark_planning_allowed"] is True
    assert by_surface["cuda_microbenchmark_plan"]["benchmark_planning_allowed"] is True
    assert by_surface["end_to_end_speedup_claim"]["benchmark_planning_allowed"] is False
    for record in records:
        assert record["benchmark_execution_allowed"] is False
        assert record["performance_claim_allowed"] is False
        assert record["speedup_claim_allowed"] is False
        assert record["gpu_benchmark_performed"] is False
