from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5by_cli_validate_and_summary_work() -> None:
    runner = CliRunner()

    uniqueness = runner.invoke(app, ["token-block", "validate-stage5by-source-digest-uniqueness"])
    assert uniqueness.exit_code == 0, uniqueness.output
    assert "stage5by_duplicate_path_count=0" in uniqueness.output

    gates = runner.invoke(app, ["token-block", "validate-stage5by-sidecar-gates"])
    assert gates.exit_code == 0, gates.output
    assert "planning_ingestion_sidecar_status=inactive_no_execution" in gates.output

    validate = runner.invoke(app, ["token-block", "validate-stage5by"])
    assert validate.exit_code == 0, validate.output
    assert "token_block_stage5by_valid=true" in validate.output

    summary = runner.invoke(app, ["token-block", "stage5by-summary"])
    assert summary.exit_code == 0, summary.output
    assert "stage_id=stage-5by" in summary.output
    assert "future_token_block_execution_remains_blocked=true" in summary.output
