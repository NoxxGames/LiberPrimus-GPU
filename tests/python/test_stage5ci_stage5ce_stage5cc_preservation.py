from test_stage5ci_common import load_yaml


def test_stage5ci_preserves_stage5ce_and_stage5cc_contracts() -> None:
    stage5ce = load_yaml("data/token-block/stage5ci-stage5ce-proposal-package-preservation.yaml")
    stage5cc = load_yaml("data/token-block/stage5ci-stage5cc-contract-preservation.yaml")

    assert stage5ce["stage5ce_proposal_package_status_preserved"] == "review_package_only"
    assert stage5ce["stage5ce_operator_deep_research_gate_design_preserved"] is True
    assert stage5cc["stage5cc_exact_citation_contract_preserved"] is True
    assert stage5cc["stage5cc_fail_closed_trigger_exact_set_preserved"] is True
    assert stage5cc["stage5cc_activation_precondition_exact_set_preserved"] is True
