from pathlib import Path

import yaml


def test_stage5ay_next_stage_selects_deep_research_review() -> None:
    payload = yaml.safe_load(Path("data/project-state/stage5ay-next-stage-decision.yaml").read_text(encoding="utf-8"))

    assert payload["selected_option_id"] == "stage5az_deep_research_review_of_bounded_preflight_manifest_and_execution_gates"
    assert payload["deep_research_review_recommended_next"] is True
    assert payload["execution_enabled"] is False
