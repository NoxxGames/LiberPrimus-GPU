from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5bd_validate_cli_reports_success() -> None:
    result = CliRunner().invoke(app, ["token-block", "validate-stage5bd"])

    assert result.exit_code == 0, result.output
    assert "token_block_stage5bd_valid=true" in result.output
    assert "run_plan_id_count=10" in result.output
    assert "real_byte_streams_generated=false" in result.output
