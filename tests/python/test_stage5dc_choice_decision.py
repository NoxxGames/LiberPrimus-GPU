from __future__ import annotations

from test_stage5dc_common import SELECTED_OPTION_ID, ensure_stage5dc_built, load_yaml


EXPECTED_OPTION_IDS = [
    "defer_for_more_review",
    "prepare_real_operator_approval_record",
    "prepare_real_deep_research_acceptance_record",
    "prepare_combined_gate_validation",
    "prepare_activation_decision_review",
    "keep_blocked_no_action",
]


def test_stage5dc_records_explicit_operator_choice() -> None:
    ensure_stage5dc_built()
    decision = load_yaml("data/token-block/stage5dc-operator-choice-decision-record.yaml")

    assert decision["operator_choice_or_pause_record_created_now"] is True
    assert decision["operator_choice_or_pause_record_valid_now"] is True
    assert decision["explicit_operator_choice_provided_now"] is True
    assert decision["explicit_pause_selected_now"] is False
    assert decision["choice_source"] == "explicit_operator_prompt_stage5dc"
    assert decision["selected_option_id"] == SELECTED_OPTION_ID


def test_stage5dc_selects_exactly_one_stage5cs_option() -> None:
    ensure_stage5dc_built()
    decision = load_yaml("data/token-block/stage5dc-operator-choice-decision-record.yaml")
    options = decision["operator_decision_options"]
    selected = [option for option in options if option["selected_now"] is True]

    assert [option["option_id"] for option in options] == EXPECTED_OPTION_IDS
    assert len(selected) == 1
    assert selected[0]["option_id"] == SELECTED_OPTION_ID
    assert decision["operator_decision_option_selected_now"] is True
    assert decision["operator_decision_option_count"] == 6
    assert decision["all_options_unselected"] is False
