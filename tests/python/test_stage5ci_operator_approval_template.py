from libreprimus.token_block.stage5ci import validate_stage5ci_operator_approval_template
from test_stage5ci_common import load_yaml, write_yaml


def test_stage5ci_operator_template_is_not_an_approval_record(tmp_path) -> None:
    counts, errors = validate_stage5ci_operator_approval_template()
    assert not errors
    assert counts["operator_approval_record_present_now"] is False
    assert counts["operator_approval_satisfied_now"] is False

    payload = load_yaml("data/token-block/stage5ci-operator-approval-record-template.yaml")
    payload["operator_approval_satisfied_now"] = True
    bad = tmp_path / "operator.yaml"
    write_yaml(bad, payload)

    _, bad_errors = validate_stage5ci_operator_approval_template(operator_template=bad)
    assert bad_errors


def test_stage5ci_operator_template_missing_required_field_fails(tmp_path) -> None:
    payload = load_yaml("data/token-block/stage5ci-operator-approval-record-template.yaml")
    payload["template_required_fields"] = []
    bad = tmp_path / "operator-missing.yaml"
    write_yaml(bad, payload)

    _, bad_errors = validate_stage5ci_operator_approval_template(operator_template=bad)
    assert bad_errors
