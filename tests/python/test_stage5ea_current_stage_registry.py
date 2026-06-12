from __future__ import annotations

from libreprimus.stage_state.current import (
    current_latest_stage_command_suffix,
    current_latest_stage_label,
    current_next_stage_label,
)
from test_stage5ea_common import ensure_stage5ea_built, load_yaml


def test_current_stage_registry_preserves_stage5ea_or_newer_stage() -> None:
    ensure_stage5ea_built()

    state = load_yaml("data/project-state/current-stage-state.yaml")

    assert state["latest_completed_stage_id"] in {
        "stage-5ea",
        "stage-5eb",
        "stage-5ec",
        "stage-5ed",
        "stage-5ee",
        "stage-5ef",
    }
    if state["latest_completed_stage_id"] == "stage-5ea":
        assert state["recommended_next_stage_id"] == "stage-5eb"
        assert current_latest_stage_label() == "Stage 5EA"
        assert current_next_stage_label() == "Stage 5EB"
        assert current_latest_stage_command_suffix() == "stage5ea"
    elif state["latest_completed_stage_id"] == "stage-5eb":
        assert state["recommended_next_stage_id"] == "stage-5ec"
        assert current_latest_stage_label() == "Stage 5EB"
        assert current_next_stage_label() == "Stage 5EC"
        assert current_latest_stage_command_suffix() == "stage5eb"
    elif state["latest_completed_stage_id"] == "stage-5ec":
        assert state["recommended_next_stage_id"] == "stage-5ed"
        assert current_latest_stage_label() == "Stage 5EC"
        assert current_next_stage_label() == "Stage 5ED"
        assert current_latest_stage_command_suffix() == "stage5ec"
    elif state["latest_completed_stage_id"] == "stage-5ed":
        assert state["recommended_next_stage_id"] == "stage-5ee"
        assert current_latest_stage_label() == "Stage 5ED"
        assert current_next_stage_label() == "Stage 5EE"
        assert current_latest_stage_command_suffix() == "stage5ed"
    elif state["latest_completed_stage_id"] == "stage-5ee":
        assert state["recommended_next_stage_id"] == "stage-5ef"
        assert current_latest_stage_label() == "Stage 5EE"
        assert current_next_stage_label() == "Stage 5EF"
        assert current_latest_stage_command_suffix() == "stage5ee"
    else:
        assert state["recommended_next_stage_id"] == "stage-5eg"
        assert current_latest_stage_label() == "Stage 5EF"
        assert current_next_stage_label() == "Stage 5EG"
        assert current_latest_stage_command_suffix() == "stage5ef"
    assert state["stage_registry_is_source_of_truth"] is True
