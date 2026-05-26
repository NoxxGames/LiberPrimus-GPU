from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ax_selects_stage5ay_after_clean_harness() -> None:
    next_stage = yaml.safe_load(
        Path("data/project-state/stage5ax-next-stage-decision.yaml").read_text(encoding="utf-8")
    )
    assert next_stage["selected_option_id"] == (
        "stage5ay_bounded_token_block_preflight_manifest_design_without_execution"
    )
    assert next_stage["selected_next_stage_title"].startswith("Stage 5AY")
    assert next_stage["execution_enabled"] is False
    assert next_stage["solve_claim"] is False
