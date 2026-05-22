from __future__ import annotations

from pathlib import Path

from libreprimus.native_candidate_batch_conformance.score_vector_conformance import build_score_vector_conformance


def test_stage5v_score_vector_records_are_stage4i_triage_only(tmp_path: Path) -> None:
    records = build_score_vector_conformance(score_vector_conformance_out=tmp_path / "score.yaml", out_dir=tmp_path / "out")
    assert len(records) == 7
    assert all(record["score_interpretation"] == "triage_only" for record in records)
    assert all(record["stage4i_compatible"] is True for record in records)
    assert all(record["solve_claim"] is False for record in records)
