from __future__ import annotations

from libreprimus.scoring_consolidation.confidence_labels import confidence_label_records, map_legacy_label
from libreprimus.scoring_consolidation.models import CONFIDENCE_LABELS


def test_stage4i_confidence_labels_are_finite_set() -> None:
    labels = [record["label"] for record in confidence_label_records()]
    assert tuple(labels) == CONFIDENCE_LABELS


def test_stage4i_confidence_labels_do_not_imply_solved() -> None:
    labels = {record["label"] for record in confidence_label_records()}
    assert "solved" not in labels
    assert "plaintext_verified" not in labels
    assert all(record["solve_claim_allowed"] is False for record in confidence_label_records())


def test_stage4i_legacy_label_mapping() -> None:
    assert map_legacy_label("lead") == "plausible_lead"
    assert map_legacy_label("weak_lead") == "weak_lead"
    assert map_legacy_label("noisy") == "noisy"
    assert map_legacy_label("inconclusive") == "inconclusive"
