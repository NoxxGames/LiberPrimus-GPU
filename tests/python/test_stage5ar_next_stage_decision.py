from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ar_next_stage_selects_deep_research_coordinate_review() -> None:
    decision = yaml.safe_load(Path("data/project-state/stage5ar-next-stage-decision.yaml").read_text(encoding="utf-8"))
    assert decision["selected_next_stage_short_name"] == "Stage 5AS"
    assert decision["deep_research_recommended_next"] is True
    assert decision["source_gap_closure_recommended_next"] is False
    assert decision["scored_experiments_recommended"] is False
    assert decision["unsolved_page_cuda_recommended"] is False
