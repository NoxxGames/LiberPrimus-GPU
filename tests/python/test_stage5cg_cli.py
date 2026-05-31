from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5cg_cli_validate_and_summary_work() -> None:
    runner = CliRunner()
    commands = [
        (
            "validate-stage5cg-operator-decision-scaffold",
            "token_block_stage5cg_operator_decision_scaffold_valid=true",
        ),
        (
            "validate-stage5cg-deep-research-decision-scaffold",
            "token_block_stage5cg_deep_research_decision_scaffold_valid=true",
        ),
        (
            "validate-stage5cg-combined-approval-gate",
            "token_block_stage5cg_combined_approval_gate_valid=true",
        ),
        (
            "validate-stage5cg-active-planning-input-decision-scaffold",
            "token_block_stage5cg_active_planning_input_decision_scaffold_valid=true",
        ),
        (
            "validate-stage5cg-stage5ce-wording-review",
            "token_block_stage5cg_stage5ce_wording_review_valid=true",
        ),
        (
            "validate-stage5cg-no-byte-stream-transition-gate",
            "token_block_stage5cg_no_byte_stream_transition_gate_valid=true",
        ),
        (
            "validate-stage5cg-no-execution-transition-gate",
            "token_block_stage5cg_no_execution_transition_gate_valid=true",
        ),
        ("validate-stage5cg-sidecar-gates", "token_block_stage5cg_sidecar_gates_valid=true"),
        ("validate-stage5cg", "token_block_stage5cg_valid=true"),
    ]
    for command, expected in commands:
        result = runner.invoke(app, ["token-block", command])
        assert result.exit_code == 0, result.output
        assert expected in result.output

    summary = runner.invoke(app, ["token-block", "stage5cg-summary"])
    assert summary.exit_code == 0, summary.output
    assert "stage_id=stage-5cg" in summary.output
    assert "approval_gate_satisfied_now=false" in summary.output
    assert "active_planning_input_authorized_now=false" in summary.output
    assert "recommended_next_stage_id=stage-5ch" in summary.output
