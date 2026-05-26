from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5aw_next_stage_selects_bounded_preflight_after_valid_repair() -> None:
    next_stage = yaml.safe_load(
        (ROOT / "data/project-state/stage5aw-next-stage-decision.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert next_stage["selected_option_id"] == (
        "stage5ax_bounded_token_block_preflight_manifest_design_without_execution"
    )
    assert next_stage["bounded_preflight_manifest_design_ready"] is True
    assert next_stage["decision_parser_followup_required"] is False
    assert next_stage["execution_enabled"] is False
