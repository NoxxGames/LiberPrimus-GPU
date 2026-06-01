from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5cq_cli_validate_and_summary_work() -> None:
    runner = CliRunner()
    build = runner.invoke(app, ["token-block", "build-stage5cq"])
    assert build.exit_code == 0, build.output
    assert "stage_id=stage-5cq" in build.output

    commands = [
        ("validate-stage5cq-stage5cp-findings", "token_block_stage5cq_stage5cp_findings_valid=true"),
        (
            "validate-stage5cq-operator-decision-package",
            "token_block_stage5cq_operator_decision_package_valid=true",
        ),
        ("validate-stage5cq-real-record-blocker", "token_block_stage5cq_real_record_blocker_valid=true"),
        ("validate-stage5cq-combined-gate", "token_block_stage5cq_combined_gate_valid=true"),
        (
            "validate-stage5cq-activation-nonauthorization",
            "token_block_stage5cq_activation_nonauthorization_valid=true",
        ),
        (
            "validate-stage5cq-stage5co-preservation",
            "token_block_stage5cq_stage5co_preservation_valid=true",
        ),
        (
            "validate-stage5cq-prior-stage-preservation",
            "token_block_stage5cq_prior_stage_preservation_valid=true",
        ),
        ("validate-stage5cq-sidecar-gates", "token_block_stage5cq_sidecar_gates_valid=true"),
        (
            "validate-stage5cq-handoff-restoration",
            "token_block_stage5cq_handoff_restoration_valid=true",
        ),
        (
            "validate-stage5cq-credential-redaction-policy",
            "token_block_stage5cq_credential_redaction_policy_valid=true",
        ),
        ("validate-stage5cq", "token_block_stage5cq_valid=true"),
    ]
    for command, expected in commands:
        result = runner.invoke(app, ["token-block", command])
        assert result.exit_code == 0, result.output
        assert expected in result.output

    summary = runner.invoke(app, ["token-block", "stage5cq-summary"])
    assert summary.exit_code == 0, summary.output
    assert "stage_id=stage-5cq" in summary.output
    assert "stage5cp_verdict=accept_with_warnings" in summary.output
    assert "operator_decision_package_status=scaffold_only" in summary.output
    assert "recommended_next_stage_id=stage-5cr" in summary.output
