from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_reporting.parity_report import build_parity_report


def test_stage5y_parity_report_compacts_stage5x_without_execution(tmp_path: Path) -> None:
    records = build_parity_report(parity_report_out=tmp_path / "parity.yaml", out_dir=tmp_path)
    assert len(records) == 3
    assert sum(1 for record in records if record["hash_match"] is True) == 2
    assert all(record["compact_summary_only"] is True for record in records)
    assert all(record["native_execution_performed"] is False for record in records)
    assert all(record["cuda_execution_performed"] is False for record in records)


def test_stage5y_parity_report_preserves_blocked_full_p56(tmp_path: Path) -> None:
    records = build_parity_report(parity_report_out=tmp_path / "parity.yaml", out_dir=tmp_path)
    blocked = [record for record in records if record["mapping_id"] == "stage5w-mapping-p56-full-fixture-blocked-v0"]
    assert len(blocked) == 1
    assert blocked[0]["blocked_in_stage5x"] is True
    assert blocked[0]["hash_match"] is False
