from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5ci_cli_validate_and_summary_work() -> None:
    runner = CliRunner()
    commands = [
        (
            "validate-stage5ci-operator-approval-template",
            "token_block_stage5ci_operator_approval_template_valid=true",
        ),
        (
            "validate-stage5ci-deep-research-acceptance-template",
            "token_block_stage5ci_deep_research_acceptance_template_valid=true",
        ),
        (
            "validate-stage5ci-combined-approval-gate",
            "token_block_stage5ci_combined_approval_gate_valid=true",
        ),
        (
            "validate-stage5ci-activation-decision-template",
            "token_block_stage5ci_activation_decision_template_valid=true",
        ),
        (
            "validate-stage5ci-negative-validation-contract",
            "token_block_stage5ci_negative_validation_contract_valid=true",
        ),
        ("validate-stage5ci-sidecar-gates", "token_block_stage5ci_sidecar_gates_valid=true"),
        ("validate-stage5ci", "token_block_stage5ci_valid=true"),
    ]
    for command, expected in commands:
        result = runner.invoke(app, ["token-block", command])
        assert result.exit_code == 0, result.output
        assert expected in result.output

    summary = runner.invoke(app, ["token-block", "stage5ci-summary"])
    assert summary.exit_code == 0, summary.output
    assert "stage_id=stage-5ci" in summary.output
    assert "combined_approval_gate_satisfied_now=false" in summary.output
    assert "activation_decision_valid_now=false" in summary.output
    assert "recommended_next_stage_id=stage-5cj" in summary.output
