from __future__ import annotations

from libreprimus.stego_controls.outguess_controls import build_positive_control_matrix


def test_stage5ap_outguess_positive_control_matrix_keeps_historical_blocked(tmp_path) -> None:
    record = build_positive_control_matrix(toolchain=tmp_path / "toolchain.yaml", out=tmp_path / "matrix.yaml", results_dir=None)
    assert record["synthetic_control_count"] == 2
    assert record["ready_historical_fixture_count"] == 0
    assert record["execution_enabled"] is False
    assert all(row["tool_executed"] is False for row in record["records"])
