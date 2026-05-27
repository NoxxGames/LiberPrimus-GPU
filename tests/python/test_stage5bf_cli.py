from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5bf_validate_cli_reports_success() -> None:
    result = CliRunner().invoke(app, ["historical-route", "validate-stage5bf"])

    assert result.exit_code == 0, result.output
    assert "stage5bf_valid=true" in result.output
    assert "high_priority_artifact_count=1043" in result.output
    assert "validation_error_count=0" in result.output
