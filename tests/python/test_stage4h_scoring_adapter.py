from __future__ import annotations

from libreprimus.cpu_batch.scoring_adapter import score_output


def test_stage4h_scoring_adapter_handles_unavailable_scoring() -> None:
    payload = score_output(None, enabled=True)
    assert payload["score_status"] == "scoring_not_available"


def test_stage4h_scoring_adapter_can_score_text() -> None:
    payload = score_output("THE WISDOM", enabled=True)
    assert payload["score_status"] == "scored"
    assert payload["no_solve_claim"] is True
