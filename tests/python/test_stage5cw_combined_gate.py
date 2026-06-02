from test_stage5cw_common import ensure_stage5cw_built, load_yaml


def test_stage5cw_combined_gate_remains_unsatisfied() -> None:
    ensure_stage5cw_built()
    payload = load_yaml("data/token-block/stage5cw-combined-gate-non-satisfaction-proof.yaml")

    assert payload["combined_approval_gate_satisfied_now"] is False
    assert payload["combined_approval_gate_authorizes_activation_now"] is False
    assert payload["approval_gate_satisfied_now"] is False
    assert payload["approval_gate_authorizes_activation_now"] is False
