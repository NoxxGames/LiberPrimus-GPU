from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5bm_cli_validate_and_summary_work() -> None:
    runner = CliRunner()

    validate_result = runner.invoke(app, ["token-block", "validate-stage5bm"])
    assert validate_result.exit_code == 0, validate_result.output
    assert "token_block_stage5bm_valid=true" in validate_result.output

    summary_result = runner.invoke(app, ["token-block", "stage5bm-summary"])
    assert summary_result.exit_code == 0, summary_result.output
    assert "string4_branch_membership_status=partial_branch_match" in summary_result.output


def test_stage5bm_cli_build_reconciliation_is_deterministic() -> None:
    result = CliRunner().invoke(app, ["token-block", "build-stage5bm-string4-reconciliation"])

    assert result.exit_code == 0, result.output
    assert "string4_branch_membership_status=partial_branch_match" in result.output
    assert "string4_unsupported_position_count=1" in result.output
