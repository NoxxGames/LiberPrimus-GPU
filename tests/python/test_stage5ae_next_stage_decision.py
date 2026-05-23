from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ae_next_stage_selects_stage5af_when_repairs_clean() -> None:
    records = yaml.safe_load(Path("data/cuda/stage5ae-corrected-bounded-p56-next-stage-decision.yaml").read_text())["records"]
    selected = [record for record in records if record["selected"] is True]
    assert len(selected) == 1
    assert selected[0]["option_id"] == "stage5af_archive_visual_numeric_source_lock"
    assert selected[0]["recommended_prompt_type"] == "Codex"
    assert selected[0]["deep_research_recommended_next"] is False
    assert all(record["execution_enabled"] is False for record in records)
