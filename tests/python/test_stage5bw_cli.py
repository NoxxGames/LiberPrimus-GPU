from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5bw_cli_validate_and_summary_work() -> None:
    runner = CliRunner()

    validate = runner.invoke(app, ["token-block", "validate-stage5bw"])
    assert validate.exit_code == 0, validate.output
    assert "token_block_stage5bw_valid=true" in validate.output

    summary = runner.invoke(app, ["token-block", "stage5bw-summary"])
    assert summary.exit_code == 0, summary.output
    assert "stage_id=stage-5bw" in summary.output
    assert "manifest_supersession_performed=false" in summary.output
