from libreprimus.token_block.stage5cm import (
    ACTIVATION_DECISION_REQUIRED_CRITERIA,
    validate_stage5cm_activation_decision_gate,
)

from test_stage5cm_common import load_yaml


def test_stage5cm_activation_decision_gate_remains_unsatisfied() -> None:
    payload = load_yaml("data/token-block/stage5cm-activation-decision-gate-hardening.yaml")
    assert payload["activation_decision_valid_now"] is False
    assert payload["activation_authorized_now"] is False
    assert payload["active_planning_input_authorized_now"] is False
    assert payload["active_planning_input_selected_now"] is False
    assert payload["new_active_planning_input_created"] is False
    assert set(payload["activation_decision_required_criteria"]) == set(
        ACTIVATION_DECISION_REQUIRED_CRITERIA
    )

    counts, errors = validate_stage5cm_activation_decision_gate()
    assert errors == []
    assert counts["stage5cm_activation_decision_gate_valid"] is True
