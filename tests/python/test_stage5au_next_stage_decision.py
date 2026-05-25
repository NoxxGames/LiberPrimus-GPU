from pathlib import Path

import yaml


def test_stage5au_next_stage_selects_manual_review_v2() -> None:
    payload = yaml.safe_load(Path("data/project-state/stage5au-next-stage-decision.yaml").read_text())
    assert payload["selected_next_stage_short_name"] == "Stage 5AV"
    assert payload["selected_next_prompt_type"] == "manual_human_review"
    assert payload["manual_human_review_recommended"] is True
    assert payload["codex_integration_next_ready"] is False
    assert payload["bounded_preflight_recommended"] is False
    assert payload["scored_experiments_recommended"] is False
    assert payload["unsolved_page_cuda_recommended"] is False
