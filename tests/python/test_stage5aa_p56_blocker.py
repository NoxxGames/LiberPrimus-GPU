from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_synthetic.p56_blocker import build_p56_blocker


def test_stage5aa_p56_and_full_p56_remain_blocked(tmp_path: Path) -> None:
    records = build_p56_blocker(p56_blocker_out=tmp_path / "p56.yaml", out_dir=tmp_path)
    statuses = {record["blocker_status"] for record in records}
    assert "p56_bounded_cuda_blocked_in_stage5aa" in statuses
    assert "blocked_full_p56_token_buffer_missing" in statuses
    assert all(record["p56_cuda_execution_performed"] is False for record in records)
    assert all(record["full_p56_cuda_execution_performed"] is False for record in records)
