from __future__ import annotations

from libreprimus.scoring_consolidation.compatibility import compatibility_records


def test_stage4i_compatibility_map_preserves_noisy_and_inconclusive_labels() -> None:
    mapping = {record["source_label"]: record["target_label"] for record in compatibility_records()}
    assert mapping["noisy"] == "noisy"
    assert mapping["inconclusive"] == "inconclusive"
    assert mapping["lead"] == "plausible_lead"


def test_stage4i_compatibility_map_has_no_solve_claims() -> None:
    assert all(record["solve_claim"] is False for record in compatibility_records())
