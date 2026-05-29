from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5bs_cli_validate_and_summary_work() -> None:
    runner = CliRunner()

    validate_result = runner.invoke(app, ["token-block", "validate-stage5bs"])
    assert validate_result.exit_code == 0, validate_result.output
    assert "token_block_stage5bs_valid=true" in validate_result.output
    assert "stage5br_verdict=accept_with_warnings" in validate_result.output
    assert "future_runner_citation_status=citation_required_fail_closed" in validate_result.output

    summary_result = runner.invoke(app, ["token-block", "stage5bs-summary"])
    assert summary_result.exit_code == 0, summary_result.output
    assert "stage_id=stage-5bs" in summary_result.output
    assert "recommended_next_stage_title=Stage 5BT" in summary_result.output
