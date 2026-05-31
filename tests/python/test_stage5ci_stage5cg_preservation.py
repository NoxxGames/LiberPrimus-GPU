from test_stage5ci_common import load_yaml


def test_stage5ci_preserves_stage5cg_scaffolds() -> None:
    payload = load_yaml("data/token-block/stage5ci-stage5cg-scaffold-preservation.yaml")
    assert payload["stage5cg_status_preserved"] is True
    assert payload["stage5cg_operator_approval_scaffold_preserved"] is True
    assert payload["stage5cg_deep_research_acceptance_scaffold_preserved"] is True
    assert payload["stage5cg_combined_approval_gate_scaffold_preserved"] is True
    assert payload["stage5cg_active_planning_input_decision_scaffold_preserved"] is True
    assert payload["stage5cg_approval_gate_satisfied_now"] is False
    assert payload["stage5cg_activation_authorized_now"] is False
