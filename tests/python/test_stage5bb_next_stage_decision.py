from pathlib import Path

import yaml


def test_stage5bb_next_stage_decision_selects_deep_research_review() -> None:
    payload = yaml.safe_load(Path("data/project-state/stage5bb-next-stage-decision.yaml").read_text())

    assert payload["selected_next_prompt_type"] == "Deep Research"
    assert payload["selected_next_stage_key"] == "stage5bc_deep_research_preflight_runner_scaffold_review"
    assert payload["execution_stage_selected"] is False
    assert payload["dwh_hash_search_selected"] is False
    assert payload["cuda_selected"] is False
