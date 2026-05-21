from __future__ import annotations

from pathlib import Path

from libreprimus.gematria_cuda_result_store.result_store_integration import build_result_store_integration
from libreprimus.gematria_cuda_result_store.score_summary_integration import build_score_summary_integration


def test_stage5p_score_summary_uses_stage4i_triage_labels(tmp_path: Path) -> None:
    result_store = tmp_path / "result-store.yaml"
    build_result_store_integration(result_store_integration_out=result_store, out_dir=tmp_path)

    records = build_score_summary_integration(
        result_store_integration=result_store,
        score_summary_integration_out=tmp_path / "score.yaml",
        out_dir=tmp_path,
    )

    assert len(records) == 5
    for record in records:
        assert record["score_summary_contract"] == "stage4i"
        assert record["confidence_label"] == "scoring_not_available"
        assert record["confidence_interpretation"] == "triage_only"
        assert record["score_as_solve_evidence_allowed"] is False
        assert record["solve_claim"] is False


def test_stage5p_score_summary_does_not_add_scorer_components(tmp_path: Path) -> None:
    result_store = tmp_path / "result-store.yaml"
    build_result_store_integration(result_store_integration_out=result_store, out_dir=tmp_path)

    records = build_score_summary_integration(
        result_store_integration=result_store,
        score_summary_integration_out=tmp_path / "score.yaml",
        out_dir=tmp_path,
    )

    assert all(record["score_components"] == [] for record in records)
    assert all(record["score_summary_available"] is False for record in records)
