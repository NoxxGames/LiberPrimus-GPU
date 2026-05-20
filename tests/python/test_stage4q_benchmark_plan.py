from __future__ import annotations

from pathlib import Path

from libreprimus.benchmark_planning.summary import build_benchmark_plan
from libreprimus.benchmark_planning.validation import validate_stage4q_results


def test_stage4q_benchmark_plan_builds_and_validates(tmp_path: Path) -> None:
    summary = build_benchmark_plan(
        out_dir=tmp_path / "out",
        plan_out=tmp_path / "plan.yaml",
        readiness_out=tmp_path / "readiness.yaml",
        summary_out=tmp_path / "summary.yaml",
    )

    counts, errors = validate_stage4q_results(
        results_dir=tmp_path / "out",
        plan_path=tmp_path / "plan.yaml",
        readiness_path=tmp_path / "readiness.yaml",
        summary_path=tmp_path / "summary.yaml",
    )
    assert errors == []
    assert counts["benchmark_plan_records"] == 5
    assert summary["cuda_implementation_added"] is False
    assert summary["future_cuda_targets_ready"] == 9
