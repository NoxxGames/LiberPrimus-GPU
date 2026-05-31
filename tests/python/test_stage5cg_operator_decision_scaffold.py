from libreprimus.token_block.stage5cg import validate_stage5cg_operator_decision_scaffold
from test_stage5cg_common import load_yaml, write_yaml


def test_stage5cg_operator_decision_scaffold_stays_unsatisfied(tmp_path) -> None:
    counts, errors = validate_stage5cg_operator_decision_scaffold()
    assert not errors
    assert counts["operator_approval_satisfied_now"] is False

    payload = load_yaml("data/token-block/stage5cg-operator-approval-decision-scaffold.yaml")
    payload["operator_approval_satisfied_now"] = True
    bad = tmp_path / "operator.yaml"
    write_yaml(bad, payload)

    _, bad_errors = validate_stage5cg_operator_decision_scaffold(operator_decision=bad)
    assert bad_errors
