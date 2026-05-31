from test_stage5ck_common import load_yaml


def test_stage5ci_templates_and_contracts_are_preserved() -> None:
    payload = load_yaml("data/token-block/stage5ck-stage5ci-template-preservation.yaml")
    assert payload["stage5ci_status_preserved"] is True
    assert payload["stage5ci_operator_approval_template_preserved"] is True
    assert payload["stage5ci_deep_research_acceptance_template_preserved"] is True
    assert payload["stage5ci_combined_approval_gate_validation_preserved"] is True
    assert payload["stage5ci_activation_decision_template_preserved"] is True
    assert payload["stage5ci_negative_validation_contract_preserved"] is True


def test_stage5ck_summary_does_not_create_real_records() -> None:
    summary = load_yaml("data/project-state/stage5ck-summary.yaml")
    assert summary["stage5ci_status_preserved"] is True
    assert summary["real_approval_records_created"] is False
    assert summary["real_deep_research_acceptance_records_created"] is False
    assert summary["real_activation_decision_records_created"] is False
    assert summary["fixture_pack_created"] is True
