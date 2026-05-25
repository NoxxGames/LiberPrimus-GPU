from pathlib import Path

import yaml


def test_stage5at_canonical_challenge_set_includes_controls_and_transition_rows() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5at-canonical-transcription-challenge-set.yaml").read_text())
    reasons = {record["review_reason"] for record in payload["records"]}
    priorities = {record["review_priority"] for record in payload["records"]}
    assert payload["ambiguity_affected_token_count"] == 203
    assert payload["non_ambiguous_control_token_count"] > 0
    assert payload["page_transition_review_item_count"] == 40
    assert "non_ambiguous_control" in reasons
    assert "control" in priorities
    assert payload["canonical_transcription_changed"] is False
