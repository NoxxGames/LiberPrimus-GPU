from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5co_cli_validate_and_summary_work() -> None:
    runner = CliRunner()
    build = runner.invoke(app, ["token-block", "build-stage5co"])
    assert build.exit_code == 0, build.output
    assert "stage_id=stage-5co" in build.output

    commands = [
        ("validate-stage5co-stage5cn-findings", "token_block_stage5co_stage5cn_findings_valid=true"),
        (
            "validate-stage5co-approval-readiness-package",
            "token_block_stage5co_approval_readiness_package_valid=true",
        ),
        (
            "validate-stage5co-real-operator-readiness",
            "token_block_stage5co_real_operator_readiness_valid=true",
        ),
        (
            "validate-stage5co-real-deep-research-readiness",
            "token_block_stage5co_real_deep_research_readiness_valid=true",
        ),
        (
            "validate-stage5co-real-combined-gate-readiness",
            "token_block_stage5co_real_combined_gate_readiness_valid=true",
        ),
        (
            "validate-stage5co-activation-transition-plan",
            "token_block_stage5co_activation_transition_plan_valid=true",
        ),
        (
            "validate-stage5co-current-missing-requirements",
            "token_block_stage5co_current_missing_requirements_valid=true",
        ),
        ("validate-stage5co-real-record-blocker", "token_block_stage5co_real_record_blocker_valid=true"),
        (
            "validate-stage5co-stage5cm-boundary-preservation",
            "token_block_stage5co_stage5cm_boundary_preservation_valid=true",
        ),
        (
            "validate-stage5co-prior-stage-preservation",
            "token_block_stage5co_prior_stage_preservation_valid=true",
        ),
        ("validate-stage5co-sidecar-gates", "token_block_stage5co_sidecar_gates_valid=true"),
        (
            "validate-stage5co-credential-redaction-policy",
            "token_block_stage5co_credential_redaction_policy_valid=true",
        ),
        ("validate-stage5co", "token_block_stage5co_valid=true"),
    ]
    for command, expected in commands:
        result = runner.invoke(app, ["token-block", command])
        assert result.exit_code == 0, result.output
        assert expected in result.output

    summary = runner.invoke(app, ["token-block", "stage5co-summary"])
    assert summary.exit_code == 0, summary.output
    assert "stage_id=stage-5co" in summary.output
    assert "stage5cn_verdict=accept_with_warnings" in summary.output
    assert "combined_approval_gate_satisfied_now=false" in summary.output
    assert "parallel_worker_cap_for_stage5co_and_later=8" in summary.output
    assert "recommended_next_stage_id=stage-5cp" in summary.output
