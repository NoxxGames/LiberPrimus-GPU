from __future__ import annotations

from pathlib import Path

from libreprimus.benchmark_planning.parity_readiness import build_parity_readiness


def test_stage4q_parity_readiness_counts_targets(tmp_path: Path) -> None:
    readiness = build_parity_readiness(out_dir=tmp_path, readiness_out=tmp_path / "readiness.yaml")

    assert sum(1 for record in readiness if record["parity_gate_status"] == "ready_for_future_cuda_planning") == 9
    assert sum(1 for record in readiness if record["benchmark_status"] == "blocked") == 2
    assert sum(1 for record in readiness if record["parity_gate_status"] == "skipped_not_cuda_target") == 3
    assert all(record["future_cuda_may_begin"] is False for record in readiness)
