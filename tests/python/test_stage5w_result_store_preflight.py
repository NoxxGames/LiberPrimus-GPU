from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_contract.result_store_preflight import build_result_store_preflight


def test_stage5w_result_store_preflight_is_stage4p_stage4i_compatible(tmp_path: Path) -> None:
    records = build_result_store_preflight(result_store_preflight_out=tmp_path / "result.yaml", out_dir=tmp_path)
    assert len(records) == 3
    assert all(record["result_store_contract"] == "stage4p" for record in records)
    assert all(record["score_summary_contract"] == "stage4i" for record in records)
    assert all(record["confidence_interpretation"] == "triage_only" for record in records)
    assert all(record["method_status_upgrade_allowed"] is False for record in records)
    assert all(record["solve_claim"] is False for record in records)

