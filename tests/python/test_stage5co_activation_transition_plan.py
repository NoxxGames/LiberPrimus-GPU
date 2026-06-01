from libreprimus.token_block.stage5co import (
    FUTURE_TRANSITION_SEQUENCE,
    validate_stage5co_activation_transition_plan,
    validate_stage5co_actual_record_rejection,
)

from test_stage5co_common import load_yaml


def test_stage5co_activation_transition_plan_is_planning_only() -> None:
    payload = load_yaml("data/token-block/stage5co-activation-decision-transition-plan.yaml")
    assert payload["transition_plan_status"] == "planning_only"
    assert payload["activation_decision_valid_now"] is False
    assert payload["active_planning_input_selected_now"] is False
    assert payload["future_transition_sequence"] == FUTURE_TRANSITION_SEQUENCE

    counts, errors = validate_stage5co_activation_transition_plan()
    assert errors == []
    assert counts["stage5co_activation_transition_plan_valid"] is True


def test_stage5co_future_transition_sequence_is_non_authorizing() -> None:
    payload = load_yaml("data/token-block/stage5co-future-transition-sequence.yaml")
    assert payload["future_transition_sequence_created"] is True
    assert payload["current_stage_authorizes_activation"] is False
    assert payload["current_stage_authorizes_execution"] is False
    assert payload["byte_stream_generation_authorized_now"] is False
    assert payload["future_transition_sequence"] == FUTURE_TRANSITION_SEQUENCE


def test_stage5co_rejects_synthetic_activation_decision_valid_now() -> None:
    errors = validate_stage5co_actual_record_rejection({"activation_decision_valid_now": True})
    assert errors
