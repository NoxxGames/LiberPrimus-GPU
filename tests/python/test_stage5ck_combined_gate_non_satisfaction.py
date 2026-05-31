from test_stage5ck_common import load_yaml


def test_combined_gate_non_satisfaction_is_explicit() -> None:
    payload = load_yaml("data/token-block/stage5ck-combined-gate-non-satisfaction-proof.yaml")
    assert payload["operator_approval_record_present_now"] is False
    assert payload["deep_research_activation_accept_record_present_now"] is False
    assert payload["combined_approval_gate_satisfied_now"] is False
    assert payload["combined_approval_gate_authorizes_activation_now"] is False
    assert payload["activation_authorized_now"] is False
