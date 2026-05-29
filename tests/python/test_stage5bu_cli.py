from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5bu_cli_validate_and_summary_work() -> None:
    runner = CliRunner()

    lineage = runner.invoke(app, ["token-block", "validate-stage5bu-lineage-paths"])
    assert lineage.exit_code == 0, lineage.output
    assert "token_block_stage5bu_lineage_paths_valid=true" in lineage.output

    validate = runner.invoke(app, ["token-block", "validate-stage5bu"])
    assert validate.exit_code == 0, validate.output
    assert "token_block_stage5bu_valid=true" in validate.output

    summary = runner.invoke(app, ["token-block", "stage5bu-summary"])
    assert summary.exit_code == 0, summary.output
    assert "stage_id=stage-5bu" in summary.output
    assert "stage5bs_validator_hardened=true" in summary.output
