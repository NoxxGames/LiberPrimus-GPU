from pathlib import Path

import yaml


def test_stage5au_decision_template_v2_is_blank() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5au-human-review-decision-template-v2.yaml").read_text())
    assert payload["template_status"] == "empty_unfilled"
    assert payload["decision_count"] == 203
    assert payload["codex_filled_decisions"] is False
    assert payload["human_review_decisions_present"] is False
    assert payload["human_review_decisions_integrated"] is False
    assert all(record["selected_token"] is None for record in payload["records"])
    assert all(record["decision"] == "unresolved" for record in payload["records"])
