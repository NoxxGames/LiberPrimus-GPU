from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5cu_cli_validate_and_summary_work() -> None:
    runner = CliRunner()
    build = runner.invoke(app, ["token-block", "build-stage5cu"])
    assert build.exit_code == 0, build.output
    assert "stage_id=stage-5cu" in build.output

    commands = [
        ("validate-stage5cu-stage5ct-findings", "token_block_stage5cu_stage5ct_findings_valid=true"),
        (
            "validate-stage5cu-decision-options-preservation",
            "token_block_stage5cu_decision_options_preservation_valid=true",
        ),
        (
            "validate-stage5cu-decision-option-negative-fixtures",
            "token_block_stage5cu_decision_option_negative_fixtures_valid=true",
        ),
        (
            "validate-stage5cu-real-decision-negative-fixtures",
            "token_block_stage5cu_real_decision_negative_fixtures_valid=true",
        ),
        (
            "validate-stage5cu-option-selection-misuse",
            "token_block_stage5cu_option_selection_misuse_valid=true",
        ),
        ("validate-stage5cu-options-nonselection", "token_block_stage5cu_options_nonselection_valid=true"),
        ("validate-stage5cu-real-record-blocker", "token_block_stage5cu_real_record_blocker_valid=true"),
        ("validate-stage5cu-combined-gate", "token_block_stage5cu_combined_gate_valid=true"),
        (
            "validate-stage5cu-activation-nonauthorization",
            "token_block_stage5cu_activation_nonauthorization_valid=true",
        ),
        (
            "validate-stage5cu-stage5cs-preservation",
            "token_block_stage5cu_stage5cs_preservation_valid=true",
        ),
        ("validate-stage5cu-stage5cq-preservation", "token_block_stage5cu_stage5cq_preservation_valid=true"),
        ("validate-stage5cu-stage5co-preservation", "token_block_stage5cu_stage5co_preservation_valid=true"),
        (
            "validate-stage5cu-prior-stage-preservation",
            "token_block_stage5cu_prior_stage_preservation_valid=true",
        ),
        ("validate-stage5cu-sidecar-gates", "token_block_stage5cu_sidecar_gates_valid=true"),
        ("validate-stage5cu-handoff-continuity", "token_block_stage5cu_handoff_continuity_valid=true"),
        (
            "validate-stage5cu-credential-redaction-policy",
            "token_block_stage5cu_credential_redaction_policy_valid=true",
        ),
        ("validate-stage5cu", "token_block_stage5cu_valid=true"),
    ]
    for command, expected in commands:
        result = runner.invoke(app, ["token-block", command])
        assert result.exit_code == 0, result.output
        assert expected in result.output

    summary = runner.invoke(app, ["token-block", "stage5cu-summary"])
    assert summary.exit_code == 0, summary.output
    assert "stage_id=stage-5cu" in summary.output
    assert "stage5ct_verdict=accept_with_warnings" in summary.output
    assert "negative_fixture_count=41" in summary.output
    assert "recommended_next_stage_id=stage-5cv" in summary.output
