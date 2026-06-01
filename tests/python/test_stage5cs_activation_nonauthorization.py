from libreprimus.token_block.stage5cs import validate_stage5cs_activation_nonauthorization

from test_stage5cs_common import ensure_stage5cs_built, load_yaml


def test_stage5cs_activation_remains_invalid_and_unauthorized() -> None:
    ensure_stage5cs_built()
    payload = load_yaml("data/token-block/stage5cs-activation-decision-nonauthorization-proof.yaml")
    assert payload["activation_decision_valid_now"] is False
    assert payload["activation_authorized_now"] is False
    assert payload["active_planning_input_authorized_now"] is False
    counts, errors = validate_stage5cs_activation_nonauthorization()
    assert not errors
    assert counts["stage5cs_activation_nonauthorization_valid"] is True
