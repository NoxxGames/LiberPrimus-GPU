from __future__ import annotations

from typer.testing import CliRunner

from libreprimus.cli import app
from libreprimus.doc_staleness.stale_current_claims import StaleCurrentFinding, StaleCurrentReport
from test_stage5eg_common import ensure_stage5eg_built


def test_stage5eg_cli_validate_and_summary_work() -> None:
    ensure_stage5eg_built()

    runner = CliRunner()
    validate = runner.invoke(app, ["token-block", "validate-stage5eg"])
    summary = runner.invoke(app, ["token-block", "stage5eg-summary"])

    assert validate.exit_code == 0, validate.output
    assert "token_block_stage5eg_valid=true" in validate.output
    assert summary.exit_code == 0
    assert "recommended_next_stage_id=stage-5eh" in summary.output


def test_stale_current_claim_cli_passes_strict() -> None:
    ensure_stage5eg_built()

    runner = CliRunner()
    result = runner.invoke(app, ["consistency", "audit-stale-current-claims", "--strict"])

    assert result.exit_code == 0, result.output
    assert "stale_current_error_count=0" in result.output


def test_stale_current_claim_report_only_escapes_non_ascii(monkeypatch) -> None:
    finding = StaleCurrentFinding(
        finding_id="synthetic",
        path="docs/emoji-\U0001f4af.md",
        line=7,
        severity="warning_domain",
        document_role="domain_doc",
        claim_type="stage_complete_claim",
        matched_text="Stage " "5AA is complete \U0001f4af",
        expected_latest_stage="stage-5ei",
        expected_next_stage="stage-6",
        suggested_fix="mark historical",
    )
    report = StaleCurrentReport(
        expected_latest_stage="stage-5ei",
        expected_next_stage="stage-6",
        scanned_path_count=1,
        skipped_path_count=0,
        findings=(finding,),
    )
    monkeypatch.setattr(
        "libreprimus.doc_staleness.stale_current_claims.audit_repository",
        lambda **_: report,
    )

    result = CliRunner().invoke(app, ["consistency", "audit-stale-current-claims", "--strict", "--report-only"])

    assert result.exit_code == 0, result.output
    assert "\U0001f4af" not in result.output
    assert "\\U0001f4af" in result.output
    assert "stale_current_claim_audit_valid=true" in result.output
