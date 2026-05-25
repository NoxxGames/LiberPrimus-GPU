from pathlib import Path

import yaml


def test_stage5at_decision_template_is_unfilled() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5at-human-review-decision-template.yaml").read_text())
    assert payload["template_status"] == "empty_unfilled"
    assert payload["codex_filled_decisions"] is False
    assert payload["canonical_transcription_changed"] is False
    assert payload["decision_count"] == 203
    assert all(record["decision"] == "unresolved" for record in payload["records"])
    assert all(record["human_selected_token"] is None for record in payload["records"])
