from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_parity.full_p56_blocker import build_full_p56_blocker


def test_stage5x_full_p56_blocker_preserves_execution_block(tmp_path: Path) -> None:
    records = build_full_p56_blocker(full_p56_blocker_out=tmp_path / "blocker.yaml", out_dir=tmp_path)
    assert len(records) == 1
    record = records[0]
    assert record["blocked_mapping_id"] == "stage5w-mapping-p56-full-fixture-blocked-v0"
    assert record["full_schedule_value_count"] == 84
    assert record["full_token_buffer_committed"] is False
    assert record["native_execution_allowed"] is False
    assert record["cuda_execution_allowed"] is False
