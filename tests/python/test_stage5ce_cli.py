from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5ce_cli_validate_and_summary_work() -> None:
    runner = CliRunner()
    commands = [
        ("validate-stage5ce-proposal-package", "token_block_stage5ce_proposal_package_valid=true"),
        ("validate-stage5ce-approval-gate", "token_block_stage5ce_approval_gate_valid=true"),
        (
            "validate-stage5ce-citation-negative-tests",
            "token_block_stage5ce_citation_negative_tests_valid=true",
        ),
        (
            "validate-stage5ce-no-byte-stream-transition-gate",
            "token_block_stage5ce_no_byte_stream_transition_gate_valid=true",
        ),
        (
            "validate-stage5ce-no-execution-transition-gate",
            "token_block_stage5ce_no_execution_transition_gate_valid=true",
        ),
        ("validate-stage5ce", "token_block_stage5ce_valid=true"),
    ]
    for command, expected in commands:
        result = runner.invoke(app, ["token-block", command])
        assert result.exit_code == 0, result.output
        assert expected in result.output

    summary = runner.invoke(app, ["token-block", "stage5ce-summary"])
    assert summary.exit_code == 0, summary.output
    assert "stage_id=stage-5ce" in summary.output
    assert "active_planning_input_authorized_now=false" in summary.output
    assert "approval_gate_satisfied_now=false" in summary.output
    assert "no_byte_stream_transition_gate_status=closed" in summary.output
