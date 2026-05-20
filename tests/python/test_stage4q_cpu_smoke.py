from __future__ import annotations

from pathlib import Path

from libreprimus.benchmark_planning.cpu_smoke import run_cpu_smoke


def test_stage4q_cpu_smoke_is_deterministic_except_timing(tmp_path: Path) -> None:
    first = run_cpu_smoke(out_dir=tmp_path / "a")
    second = run_cpu_smoke(out_dir=tmp_path / "b")

    stripped_first = [{k: v for k, v in record.items() if k != "diagnostic_elapsed_ns"} for record in first]
    stripped_second = [{k: v for k, v in record.items() if k != "diagnostic_elapsed_ns"} for record in second]
    assert stripped_first == stripped_second
    assert all(record["performance_claim"] is False for record in first)
    assert all(record["gpu_benchmark_performed"] is False for record in first)
