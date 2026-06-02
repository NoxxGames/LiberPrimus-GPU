from test_stage5cw_common import ensure_stage5cw_built, load_yaml


def test_stage5cw_activation_remains_invalid_and_unauthorized() -> None:
    ensure_stage5cw_built()
    payload = load_yaml("data/token-block/stage5cw-activation-decision-nonauthorization-proof.yaml")

    assert payload["activation_decision_valid_now"] is False
    assert payload["activation_authorized_now"] is False
    assert payload["active_planning_input_authorized_now"] is False
    assert payload["active_planning_input_selected_now"] is False
