from libreprimus.token_block.stage5cq import (
    validate_stage5cq_activation_nonauthorization,
    validate_stage5cq_actual_record_rejection,
)

from test_stage5cq_common import ensure_stage5cq_built, load_yaml


def test_stage5cq_activation_decision_remains_invalid() -> None:
    ensure_stage5cq_built()
    payload = load_yaml("data/token-block/stage5cq-activation-decision-nonauthorization-proof.yaml")
    assert payload["activation_decision_valid_now"] is False
    assert payload["activation_authorized_now"] is False
    assert payload["active_planning_input_authorized_now"] is False
    counts, errors = validate_stage5cq_activation_nonauthorization()
    assert not errors
    assert counts["stage5cq_activation_nonauthorization_valid"] is True


def test_stage5cq_rejects_activation_valid_now() -> None:
    assert validate_stage5cq_actual_record_rejection({"activation_decision_valid_now": True})
