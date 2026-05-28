from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5bn_cli_validate_and_summary_work() -> None:
    runner = CliRunner()

    validate_result = runner.invoke(app, ["token-block", "validate-stage5bn"])
    assert validate_result.exit_code == 0, validate_result.output
    assert "token_block_stage5bn_valid=true" in validate_result.output
    assert "spreadsheet_supports_0l=true" in validate_result.output

    summary_result = runner.invoke(app, ["token-block", "show-stage5bn-summary"])
    assert summary_result.exit_code == 0, summary_result.output
    assert "unsupported_position_closure_status=closed_spreadsheet_support_found" in summary_result.output


def test_stage5bn_cli_build_is_deterministic() -> None:
    result = CliRunner().invoke(app, ["token-block", "build-stage5bn-unsupported-position-review"])

    assert result.exit_code == 0, result.output
    assert "target_token_index_0_based=199" in result.output
    assert "stage5aw_supports_0l=false" in result.output
    assert "spreadsheet_supports_0l=true" in result.output
