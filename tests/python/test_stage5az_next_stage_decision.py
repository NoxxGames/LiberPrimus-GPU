from pathlib import Path

import yaml


def test_stage5az_next_stage_is_stage5ba_deep_research_review() -> None:
    payload = yaml.safe_load(Path("data/project-state/stage5az-next-stage-decision.yaml").read_text(encoding="utf-8"))

    assert payload["selected_next_stage_title"].startswith("Stage 5BA - Deep Research review")
    assert payload["execution_enabled"] is False
    assert payload["solve_claim"] is False
