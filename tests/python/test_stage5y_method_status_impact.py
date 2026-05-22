from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_reporting.method_status_impact import build_method_status_impact


def test_stage5y_method_status_impact_never_marks_solved(tmp_path: Path) -> None:
    records = build_method_status_impact(method_status_impact_out=tmp_path / "method.yaml", out_dir=tmp_path)
    assert len(records) == 5
    assert all(record["method_status_upgraded"] is False for record in records)
    assert all(record["method_status_upgrade_allowed"] is False for record in records)
    assert all(record["marked_solved"] is False for record in records)
    assert any(record["method_family_id"] == "unsolved_page_cuda" for record in records)
