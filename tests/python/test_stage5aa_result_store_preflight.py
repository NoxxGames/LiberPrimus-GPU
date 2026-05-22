from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_synthetic.result_store_preflight import build_result_store_preflight


def test_stage5aa_result_store_preflight_is_compact_metadata_only(tmp_path: Path) -> None:
    records = build_result_store_preflight(result_store_preflight_out=tmp_path / "result.yaml", out_dir=tmp_path)
    assert {record["compatibility_contract"] for record in records} == {"stage4p", "stage4i"}
    assert all(record["compact_metadata_only"] is True for record in records)
    assert all(record["generated_outputs_committed"] is False for record in records)
    assert all(record["solve_claim"] is False for record in records)
