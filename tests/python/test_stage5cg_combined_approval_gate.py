from libreprimus.token_block.stage5cg import validate_stage5cg_combined_approval_gate
from test_stage5cg_common import load_yaml, write_yaml


def test_stage5cg_combined_approval_gate_requires_both_future_records(tmp_path) -> None:
    counts, errors = validate_stage5cg_combined_approval_gate()
    assert not errors
    assert counts["approval_gate_satisfied_now"] is False
    assert counts["approval_gate_authorizes_activation_now"] is False

    payload = load_yaml("data/token-block/stage5cg-combined-approval-decision-gate-scaffold.yaml")
    payload["approval_gate_authorizes_activation_now"] = True
    bad = tmp_path / "combined.yaml"
    write_yaml(bad, payload)

    _, bad_errors = validate_stage5cg_combined_approval_gate(combined_gate=bad)
    assert bad_errors
