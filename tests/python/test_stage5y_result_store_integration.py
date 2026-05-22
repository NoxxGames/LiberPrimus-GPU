from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_reporting.parity_report import build_parity_report
from libreprimus.prime_minus_one_native_reporting.result_store_integration import build_result_store_integration


def test_stage5y_result_store_integration_is_stage4p_metadata_only(tmp_path: Path) -> None:
    parity = tmp_path / "parity.yaml"
    result = tmp_path / "result.yaml"
    build_parity_report(parity_report_out=parity, out_dir=tmp_path)
    records = build_result_store_integration(
        parity_report=parity,
        result_store_integration_out=result,
        out_dir=tmp_path,
    )
    assert len(records) == 3
    assert {record["stage4p_compatibility"] for record in records} == {"compatible"}
    assert all(record["compact_summary_only"] is True for record in records)
    assert all(record["generated_body_publication_allowed"] is False for record in records)
    assert all(record["method_status_upgrade_allowed"] is False for record in records)
