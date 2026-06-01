from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5cs_cli_validate_and_summary_work() -> None:
    runner = CliRunner()
    build = runner.invoke(app, ["token-block", "build-stage5cs"])
    assert build.exit_code == 0, build.output
    assert "stage_id=stage-5cs" in build.output

    commands = [
        ("validate-stage5cs-stage5cr-findings", "token_block_stage5cs_stage5cr_findings_valid=true"),
        (
            "validate-stage5cs-operator-decision-readiness",
            "token_block_stage5cs_operator_decision_readiness_valid=true",
        ),
        ("validate-stage5cs-decision-options", "token_block_stage5cs_decision_options_valid=true"),
        (
            "validate-stage5cs-options-nonselection",
            "token_block_stage5cs_options_nonselection_valid=true",
        ),
        ("validate-stage5cs-real-record-blocker", "token_block_stage5cs_real_record_blocker_valid=true"),
        ("validate-stage5cs-combined-gate", "token_block_stage5cs_combined_gate_valid=true"),
        (
            "validate-stage5cs-activation-nonauthorization",
            "token_block_stage5cs_activation_nonauthorization_valid=true",
        ),
        (
            "validate-stage5cs-stage5cq-preservation",
            "token_block_stage5cs_stage5cq_preservation_valid=true",
        ),
        (
            "validate-stage5cs-stage5co-preservation",
            "token_block_stage5cs_stage5co_preservation_valid=true",
        ),
        (
            "validate-stage5cs-prior-stage-preservation",
            "token_block_stage5cs_prior_stage_preservation_valid=true",
        ),
        ("validate-stage5cs-sidecar-gates", "token_block_stage5cs_sidecar_gates_valid=true"),
        (
            "validate-stage5cs-handoff-continuity",
            "token_block_stage5cs_handoff_continuity_valid=true",
        ),
        (
            "validate-stage5cs-credential-redaction-policy",
            "token_block_stage5cs_credential_redaction_policy_valid=true",
        ),
        ("validate-stage5cs", "token_block_stage5cs_valid=true"),
    ]
    for command, expected in commands:
        result = runner.invoke(app, ["token-block", command])
        assert result.exit_code == 0, result.output
        assert expected in result.output

    summary = runner.invoke(app, ["token-block", "stage5cs-summary"])
    assert summary.exit_code == 0, summary.output
    assert "stage_id=stage-5cs" in summary.output
    assert "stage5cr_verdict=accept_with_warnings" in summary.output
    assert "operator_decision_option_count=6" in summary.output
    assert "recommended_next_stage_id=stage-5ct" in summary.output
