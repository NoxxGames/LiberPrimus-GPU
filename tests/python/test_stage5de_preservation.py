from __future__ import annotations

from test_stage5de_common import SELECTED_OPTION_ID, ensure_stage5de_built, load_yaml


def test_stage5de_preserves_stage5dc_choice_and_selected_option() -> None:
    ensure_stage5de_built()
    selected = load_yaml("data/token-block/stage5de-stage5dc-selected-option-preservation.yaml")
    choice = load_yaml("data/token-block/stage5de-stage5dc-choice-record-preservation.yaml")

    assert selected["stage5dc_selected_option_preserved"] is True
    assert selected["selected_option_id"] == SELECTED_OPTION_ID
    assert selected["selected_option_count"] == 1
    assert selected["unselected_option_count"] == 5
    assert selected["selected_option_authorizes_execution_now"] is False
    assert choice["stage5dc_choice_record_preserved"] is True
    assert choice["stage5da_selects_operator_choice"] is False


def test_stage5de_preserves_unselected_options() -> None:
    ensure_stage5de_built()
    unselected = load_yaml("data/token-block/stage5de-unselected-options-preservation.yaml")

    assert unselected["unselected_option_count"] == 5
    assert SELECTED_OPTION_ID not in unselected["unselected_option_ids"]
    assert all(option["selected_now"] is False for option in unselected["unselected_options"])
    assert all(option["authorizes_execution_now"] is False for option in unselected["unselected_options"])


def test_stage5de_preserves_stage5bd_and_active_lineage() -> None:
    ensure_stage5de_built()
    summary = load_yaml("data/project-state/stage5de-summary.yaml")

    assert summary["stage5bd_run_plan_id_count"] == 10
    assert summary["stage5bd_run_plan_ids_changed"] is False
    assert summary["active_lineage_record_count"] == 8
    assert summary["correct_stage5aw_path_included"] is True
    assert summary["deprecated_stage5aw_path_absent"] is True
