from __future__ import annotations

from pathlib import Path

from libreprimus.benchmark_planning.environment import build_environment_record


def test_stage4q_environment_record_is_cpu_only(tmp_path: Path) -> None:
    record = build_environment_record(out_dir=tmp_path)

    assert record["cuda_used"] is False
    assert record["gpu_benchmark_performed"] is False
    assert record["absolute_paths_committed"] is False
    assert (tmp_path / "benchmark_environment.json").is_file()
