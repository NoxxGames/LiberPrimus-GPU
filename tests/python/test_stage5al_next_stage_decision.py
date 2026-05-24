from __future__ import annotations

import yaml

from libreprimus.paths import repo_root


def test_next_stage_selects_stage5am_deep_research_prompt() -> None:
    decision = yaml.safe_load((repo_root() / "data/source-harvester/stage5al-next-stage-decision.yaml").read_text(encoding="utf-8"))
    selected = [record for record in decision["records"] if record["selected"]]
    assert len(selected) == 1
    assert selected[0]["recommended_next_prompt_type"] == "Deep Research"
    assert selected[0]["recommended_next_stage_title"] == "Stage 5AM - Deep Research source inventory and reliability prompt"
    assert selected[0]["deep_research_recommended_next"] is True
    assert selected[0]["website_expansion_recommended_next"] is False
    assert selected[0]["scored_experiment_recommended_next"] is False
    assert selected[0]["unsolved_page_cuda_recommended_next"] is False
