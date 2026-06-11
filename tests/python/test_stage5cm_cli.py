from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5cm_cli_validate_and_summary_work() -> None:
    runner = CliRunner()
    commands = [
        (
            "validate-stage5cm-approval-readiness-boundary",
            "token_block_stage5cm_approval_readiness_boundary_valid=true",
        ),
        (
            "validate-stage5cm-fixture-real-boundary",
            "token_block_stage5cm_fixture_real_boundary_valid=true",
        ),
        (
            "validate-stage5cm-end-to-end-readiness-boundary",
            "token_block_stage5cm_end_to_end_readiness_boundary_valid=true",
        ),
        (
            "validate-stage5cm-real-approval-readiness",
            "token_block_stage5cm_real_approval_readiness_valid=true",
        ),
        (
            "validate-stage5cm-activation-decision-gate",
            "token_block_stage5cm_activation_decision_gate_valid=true",
        ),
        (
            "validate-stage5cm-credential-redaction-policy",
            "token_block_stage5cm_credential_redaction_policy_valid=true",
        ),
        ("validate-stage5cm-sidecar-gates", "token_block_stage5cm_sidecar_gates_valid=true"),
        ("validate-stage5cm", "token_block_stage5cm_valid=true"),
    ]
    for command, expected in commands:
        result = runner.invoke(app, ["token-block", command])
        assert result.exit_code == 0, result.output
        assert expected in result.output

    summary = runner.invoke(app, ["token-block", "stage5cm-summary"])
    assert summary.exit_code == 0, summary.output
    assert "stage_id=stage-5cm" in summary.output
    assert "stage5cl_verdict=accept_with_warnings" in summary.output
    assert "combined_approval_gate_satisfied_now=false" in summary.output
    assert "parallel_worker_cap_for_stage5cm_and_later=8" in summary.output
    assert "recommended_next_stage_id=stage-5cn" in summary.output
