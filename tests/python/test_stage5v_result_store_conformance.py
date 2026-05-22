from __future__ import annotations

from pathlib import Path

from libreprimus.native_candidate_batch_conformance.result_store_conformance import build_result_store_conformance


def test_stage5v_result_store_conformance_is_compact_only(tmp_path: Path) -> None:
    records = build_result_store_conformance(result_store_conformance_out=tmp_path / "result.yaml", out_dir=tmp_path / "out")
    assert len(records) == 3
    assert all(record["compact_summary_only"] is True for record in records)
    assert all(record["generated_body_committed"] is False for record in records)
    assert all(record["method_status_upgraded"] is False for record in records)
