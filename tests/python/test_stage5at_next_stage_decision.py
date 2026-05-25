from pathlib import Path

import yaml


def test_stage5at_next_stage_selects_manual_review_without_decisions() -> None:
    summary = yaml.safe_load(Path("data/project-state/stage5at-summary.yaml").read_text())
    next_stage = yaml.safe_load(Path("data/project-state/stage5at-next-stage-decision.yaml").read_text())
    assert summary["human_review_decisions_present"] is False
    assert summary["human_review_decisions_integrated"] is False
    assert next_stage["selected_next_stage_short_name"] == "Stage 5AU"
    assert next_stage["selected_next_prompt_type"] == "manual_human_review"
    assert next_stage["manual_human_review_recommended"] is True
    assert next_stage["unsolved_page_cuda_recommended"] is False
