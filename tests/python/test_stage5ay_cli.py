from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5ay_validate_cli_works() -> None:
    result = CliRunner().invoke(app, ["token-block", "validate-stage5ay"])

    assert result.exit_code == 0, result.output
    assert "token_block_stage5ay_valid=true" in result.output
    assert "validation_error_count=0" in result.output
