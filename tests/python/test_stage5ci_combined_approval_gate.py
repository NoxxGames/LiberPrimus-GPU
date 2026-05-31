from libreprimus.token_block.stage5ci import validate_stage5ci_combined_approval_gate
from test_stage5ci_common import load_yaml, write_yaml


def test_stage5ci_combined_gate_requires_both_future_records(tmp_path) -> None:
    counts, errors = validate_stage5ci_combined_approval_gate()
    assert not errors
    assert counts["combined_approval_gate_satisfied_now"] is False
    assert counts["approval_gate_authorizes_activation_now"] is False

    payload = load_yaml("data/token-block/stage5ci-combined-approval-gate-validation-preflight.yaml")
    payload["required_approval_record_types"] = ["future_operator_approval_record"]
    bad = tmp_path / "combined.yaml"
    write_yaml(bad, payload)

    _, bad_errors = validate_stage5ci_combined_approval_gate(combined_gate=bad)
    assert bad_errors


def test_stage5ci_template_misread_as_approval_fails(tmp_path) -> None:
    payload = load_yaml("data/token-block/stage5ci-combined-approval-gate-validation-preflight.yaml")
    payload["approval_gate_satisfied_now"] = True
    bad = tmp_path / "combined-satisfied.yaml"
    write_yaml(bad, payload)

    _, bad_errors = validate_stage5ci_combined_approval_gate(combined_gate=bad)
    assert bad_errors
