from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5bb_validate_cli_reports_success() -> None:
    result = CliRunner().invoke(app, ["token-block", "validate-stage5bb"])

    assert result.exit_code == 0, result.output
    assert "token_block_stage5bb_valid=true" in result.output
    assert "runner_execution_created=false" in result.output
    assert "real_byte_streams_generated=false" in result.output
