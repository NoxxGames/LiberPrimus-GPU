from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5cc_cli_validate_and_summary_work() -> None:
    runner = CliRunner()
    commands = [
        ("validate-stage5cc-citation-contract", "token_block_stage5cc_citation_contract_valid=true"),
        (
            "validate-stage5cc-fail-closed-triggers",
            "token_block_stage5cc_fail_closed_triggers_valid=true",
        ),
        (
            "validate-stage5cc-activation-preconditions",
            "token_block_stage5cc_activation_preconditions_valid=true",
        ),
        (
            "validate-stage5cc-active-planning-input-preflight",
            "token_block_stage5cc_active_planning_input_preflight_valid=true",
        ),
        (
            "validate-stage5cc-no-byte-stream-transition-gate",
            "token_block_stage5cc_no_byte_stream_transition_gate_valid=true",
        ),
        (
            "validate-stage5cc-no-execution-transition-gate",
            "token_block_stage5cc_no_execution_transition_gate_valid=true",
        ),
        ("validate-stage5cc-sidecar-gates", "token_block_stage5cc_sidecar_gates_valid=true"),
        ("validate-stage5cc", "token_block_stage5cc_valid=true"),
    ]
    for command, expected in commands:
        result = runner.invoke(app, ["token-block", command])
        assert result.exit_code == 0, result.output
        assert expected in result.output

    summary = runner.invoke(app, ["token-block", "stage5cc-summary"])
    assert summary.exit_code == 0, summary.output
    assert "stage_id=stage-5cc" in summary.output
    assert "active_planning_input_authorized_now=false" in summary.output
    assert "no_byte_stream_transition_gate_status=closed" in summary.output
