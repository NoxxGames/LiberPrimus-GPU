from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_parity.native_execution import build_native_run_records
from libreprimus.prime_minus_one_native_parity.parity_records import build_parity_records
from libreprimus.prime_minus_one_native_parity.result_store_preflight import build_result_store_preflight


def test_stage5x_result_store_preflight_is_compact_and_stage4p_compatible(tmp_path: Path) -> None:
    run = tmp_path / "run.yaml"
    parity = tmp_path / "parity.yaml"
    result = tmp_path / "result.yaml"
    build_native_run_records(native_run_out=run, out_dir=tmp_path)
    build_parity_records(native_run=run, native_parity_out=parity, out_dir=tmp_path)
    records = build_result_store_preflight(native_parity=parity, result_store_preflight_out=result, out_dir=tmp_path)
    assert len(records) == 3
    assert all(record["compact_summary_only"] is True for record in records)
    assert all(record["generated_body_publication_allowed"] is False for record in records)
    assert all(record["result_store_contract"] == "stage4p" for record in records)
    assert all(record["score_summary_contract"] == "stage4i" for record in records)
