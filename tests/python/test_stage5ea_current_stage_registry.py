from __future__ import annotations

from libreprimus.stage_state.current import (
    current_latest_stage_command_suffix,
    current_latest_stage_label,
    current_next_stage_label,
)
from test_stage5ea_common import ensure_stage5ea_built, load_yaml


def test_current_stage_registry_points_to_stage5ea_and_stage5eb() -> None:
    ensure_stage5ea_built()

    state = load_yaml("data/project-state/current-stage-state.yaml")

    assert state["latest_completed_stage_id"] == "stage-5ea"
    assert state["recommended_next_stage_id"] == "stage-5eb"
    assert state["stage_registry_is_source_of_truth"] is True
    assert current_latest_stage_label() == "Stage 5EA"
    assert current_next_stage_label() == "Stage 5EB"
    assert current_latest_stage_command_suffix() == "stage5ea"
