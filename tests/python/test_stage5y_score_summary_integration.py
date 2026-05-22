from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_reporting.parity_report import build_parity_report
from libreprimus.prime_minus_one_native_reporting.score_summary_integration import build_score_summary_integration


def test_stage5y_score_summary_uses_stage4i_labels(tmp_path: Path) -> None:
    parity = tmp_path / "parity.yaml"
    score = tmp_path / "score.yaml"
    build_parity_report(parity_report_out=parity, out_dir=tmp_path)
    records = build_score_summary_integration(
        parity_report=parity,
        score_summary_integration_out=score,
        out_dir=tmp_path,
    )
    labels = {record["confidence_label"] for record in records}
    assert labels == {"positive_control_like", "scoring_not_available"}
    assert all(record["score_summary_contract"] == "stage4i" for record in records)
    assert all(record["confidence_interpretation"] == "triage_only" for record in records)
    assert all(record["solve_claim"] is False for record in records)
