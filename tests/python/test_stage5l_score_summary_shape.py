from __future__ import annotations

from libreprimus.gematria_solved_fixture_mapping.export import read_record_set
from libreprimus.gematria_solved_fixture_mapping.models import ALLOWED_CONFIDENCE_LABELS
from libreprimus.paths import repo_root


def test_score_summary_shape_uses_stage4i_triage_labels() -> None:
    records = read_record_set(repo_root() / "data/cuda/stage5l-gematria-solved-fixture-score-summary-shape.yaml")
    record = records[0]
    assert record["score_summary_contract"] == "stage4i"
    assert record["score_interpretation"] == "triage_only"
    assert set(record["allowed_confidence_labels"]) == set(ALLOWED_CONFIDENCE_LABELS)
    assert record["confidence_label_solve_evidence_allowed"] is False
