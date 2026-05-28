from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5bq_cli_validate_and_summary_work() -> None:
    runner = CliRunner()

    validate_result = runner.invoke(app, ["token-block", "validate-stage5bq"])
    assert validate_result.exit_code == 0, validate_result.output
    assert "token_block_stage5bq_valid=true" in validate_result.output
    assert "string4_planning_context_status=inactive_branch_context_only" in validate_result.output

    summary_result = runner.invoke(app, ["token-block", "stage5bq-summary"])
    assert summary_result.exit_code == 0, summary_result.output
    assert "recommended_next_stage_title=Stage 5BR" in summary_result.output


def test_stage5bq_cli_build_is_raw_data_free(tmp_path: Path) -> None:
    out = tmp_path / "records"
    results = tmp_path / "results"
    result = CliRunner().invoke(
        app,
        [
            "token-block",
            "build-stage5bq-planning-integration",
            "--results-dir",
            str(results),
            "--out-findings",
            str(out / "findings.yaml"),
            "--out-review-packaging-warning",
            str(out / "review-warning.yaml"),
            "--out-string4-context",
            str(out / "context.yaml"),
            "--out-sidecar-status",
            str(out / "sidecar.yaml"),
            "--out-dry-run-constraint",
            str(out / "constraint.yaml"),
            "--out-no-active-ingestion",
            str(out / "no-active.yaml"),
            "--out-future-requirements",
            str(out / "requirements.yaml"),
            "--out-active-preservation",
            str(out / "active.yaml"),
            "--out-stage5bd-preservation",
            str(out / "stage5bd.yaml"),
            "--out-future-impact",
            str(out / "impact.yaml"),
            "--out-source-gap",
            str(out / "gap.yaml"),
            "--out-dwh",
            str(out / "dwh.yaml"),
            "--out-guardrail",
            str(out / "guardrail.yaml"),
            "--out-handoff",
            str(out / "handoff.yaml"),
            "--out-summary",
            str(out / "summary.yaml"),
            "--out-next-stage",
            str(out / "next.yaml"),
        ],
    )

    assert result.exit_code == 0, result.output
    assert "stage5bp_verdict=accept_with_warnings" in result.output
    assert "string4_active_input_allowed=false" in result.output
    assert (results / "summary.json").is_file()
