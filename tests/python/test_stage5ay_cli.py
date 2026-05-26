from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5ay_validate_cli_works_without_generated_outputs(tmp_path: Path) -> None:
    result = CliRunner().invoke(app, ["token-block", "validate-stage5ay", "--results-dir", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert "token_block_stage5ay_valid=true" in result.output
    assert "validation_error_count=0" in result.output
    assert "stage5ay_generated_summary_present=false" in result.output
