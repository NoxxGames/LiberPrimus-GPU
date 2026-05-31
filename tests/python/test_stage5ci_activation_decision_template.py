from libreprimus.token_block.stage5ci import validate_stage5ci_activation_decision_template
from test_stage5ci_common import load_yaml, write_yaml


def test_stage5ci_activation_decision_template_stays_inactive(tmp_path) -> None:
    counts, errors = validate_stage5ci_activation_decision_template()
    assert not errors
    assert counts["activation_decision_valid_now"] is False
    assert counts["active_planning_input_authorized_now"] is False

    payload = load_yaml(
        "data/token-block/stage5ci-active-planning-input-activation-decision-template.yaml"
    )
    payload["activation_decision_valid_now"] = True
    bad = tmp_path / "activation.yaml"
    write_yaml(bad, payload)

    _, bad_errors = validate_stage5ci_activation_decision_template(activation_template=bad)
    assert bad_errors


def test_stage5ci_dry_run_and_supersession_authorization_fail(tmp_path) -> None:
    payload = load_yaml(
        "data/token-block/stage5ci-active-planning-input-activation-decision-template.yaml"
    )
    payload["dry_run_ingestion_authorized_now"] = True
    payload["manifest_supersession_authorized_now"] = True
    bad = tmp_path / "activation-authorized.yaml"
    write_yaml(bad, payload)

    _, bad_errors = validate_stage5ci_activation_decision_template(activation_template=bad)
    assert bad_errors
