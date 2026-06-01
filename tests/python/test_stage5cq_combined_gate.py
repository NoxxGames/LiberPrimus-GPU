from libreprimus.token_block.stage5cq import validate_stage5cq_combined_gate

from test_stage5cq_common import ensure_stage5cq_built, load_yaml


def test_stage5cq_combined_gate_remains_unsatisfied() -> None:
    ensure_stage5cq_built()
    payload = load_yaml("data/token-block/stage5cq-combined-gate-non-satisfaction-proof.yaml")
    assert payload["combined_approval_gate_satisfied_now"] is False
    assert payload["combined_approval_gate_authorizes_activation_now"] is False
    counts, errors = validate_stage5cq_combined_gate()
    assert not errors
    assert counts["stage5cq_combined_gate_valid"] is True
