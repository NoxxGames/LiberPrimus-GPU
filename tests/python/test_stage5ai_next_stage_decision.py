from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ai_next_stage_decision_is_deep_research_prompt() -> None:
    payload = yaml.safe_load(Path("data/source-harvester/stage5ai-next-stage-decision.yaml").read_text(encoding="utf-8"))
    selected = [record for record in payload["records"] if record["selected"]]
    assert len(selected) == 1
    assert selected[0]["option_id"] == "stage5aj_deep_research_source_inventory_and_reliability_prompt"
    assert selected[0]["deep_research_recommended_next"] is True
    assert selected[0]["scored_experiment_recommended_next"] is False
    assert selected[0]["unsolved_page_cuda_recommended_next"] is False
    assert selected[0]["website_expansion_recommended_next"] is False
