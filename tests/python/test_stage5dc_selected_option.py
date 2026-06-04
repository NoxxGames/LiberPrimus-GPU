from __future__ import annotations

from test_stage5dc_common import SELECTED_OPTION_ID, ensure_stage5dc_built, load_yaml


def test_stage5dc_selected_option_is_record_preparation_only() -> None:
    ensure_stage5dc_built()
    selected = load_yaml("data/token-block/stage5dc-selected-option-record.yaml")

    assert selected["option_id"] == SELECTED_OPTION_ID
    assert selected["selected_now"] is True
    assert selected["future_action_class"] == "record_preparation_only"
    assert selected["authorizes_real_operator_approval_record_creation_now"] is False
    assert selected["authorizes_real_approval_now"] is False
    assert selected["authorizes_deep_research_acceptance_now"] is False
    assert selected["authorizes_combined_gate_validation_now"] is False
    assert selected["authorizes_activation_decision_now"] is False
    assert selected["authorizes_activation_now"] is False
    assert selected["authorizes_active_planning_input_now"] is False
    assert selected["authorizes_dry_run_ingestion_now"] is False
    assert selected["authorizes_byte_stream_generation_now"] is False
    assert selected["authorizes_execution_now"] is False


def test_stage5dc_other_options_remain_unselected() -> None:
    ensure_stage5dc_built()
    unselected = load_yaml("data/token-block/stage5dc-unselected-options-preservation.yaml")

    assert unselected["unselected_option_count"] == 5
    assert SELECTED_OPTION_ID not in unselected["unselected_option_ids"]
    assert all(option["selected_now"] is False for option in unselected["unselected_options"])
