from libreprimus.token_block.stage5cu import validate_stage5cu_activation_nonauthorization

from test_stage5cu_common import ensure_stage5cu_built, load_yaml


def test_stage5cu_activation_remains_invalid_and_unauthorized() -> None:
    ensure_stage5cu_built()
    payload = load_yaml("data/token-block/stage5cu-activation-decision-nonauthorization-proof.yaml")
    assert payload["activation_decision_valid_now"] is False
    assert payload["activation_authorized_now"] is False
    assert payload["active_planning_input_authorized_now"] is False
    counts, errors = validate_stage5cu_activation_nonauthorization()
    assert not errors
    assert counts["stage5cu_activation_nonauthorization_valid"] is True
