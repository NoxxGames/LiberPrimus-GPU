from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_synthetic.scored_experiment_deferral import build_scored_experiment_deferral


def test_stage5aa_scored_experiments_are_deferred(tmp_path: Path) -> None:
    records = build_scored_experiment_deferral(scored_experiment_deferral_out=tmp_path / "scored.yaml", out_dir=tmp_path)
    assert len(records) == 6
    assert all(record["execution_enabled"] is False for record in records)
    assert all(record["scored_experiment_executed"] is False for record in records)
    assert all(record["benchmark_allowed"] is False for record in records)
    assert all(record["solve_claim"] is False for record in records)
