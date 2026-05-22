from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_reporting.full_p56_blocker import build_full_p56_blocker_preservation


def test_stage5y_full_p56_blocker_is_preserved(tmp_path: Path) -> None:
    records = build_full_p56_blocker_preservation(
        full_p56_blocker_preservation_out=tmp_path / "blocker.yaml",
        out_dir=tmp_path,
    )
    assert len(records) == 1
    record = records[0]
    assert record["blocker_status"] == "enforced"
    assert record["full_token_buffer_committed"] is False
    assert record["full_p56_native_execution_allowed"] is False
    assert record["full_p56_cuda_execution_allowed"] is False
    assert record["full_schedule_value_count"] == 84
