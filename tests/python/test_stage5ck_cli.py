from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5ck_cli_validate_and_summary_work() -> None:
    runner = CliRunner()
    commands = [
        ("validate-stage5ck-operator-fixtures", "token_block_stage5ck_operator_fixtures_valid=true"),
        (
            "validate-stage5ck-deep-research-fixtures",
            "token_block_stage5ck_deep_research_fixtures_valid=true",
        ),
        (
            "validate-stage5ck-activation-decision-fixtures",
            "token_block_stage5ck_activation_decision_fixtures_valid=true",
        ),
        (
            "validate-stage5ck-negative-validation-matrix",
            "token_block_stage5ck_negative_validation_matrix_valid=true",
        ),
        ("validate-stage5ck-review-package", "token_block_stage5ck_review_package_valid=true"),
        ("validate-stage5ck-sidecar-gates", "token_block_stage5ck_sidecar_gates_valid=true"),
        ("validate-stage5ck", "token_block_stage5ck_valid=true"),
    ]
    for command, expected in commands:
        result = runner.invoke(app, ["token-block", command])
        assert result.exit_code == 0, result.output
        assert expected in result.output

    summary = runner.invoke(app, ["token-block", "stage5ck-summary"])
    assert summary.exit_code == 0, summary.output
    assert "stage_id=stage-5ck" in summary.output
    assert "fixture_pack_created=true" in summary.output
    assert "combined_approval_gate_satisfied_now=false" in summary.output
    assert "recommended_next_stage_id=stage-5cl" in summary.output
