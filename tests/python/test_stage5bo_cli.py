from pathlib import Path

import yaml
from typer.testing import CliRunner

from libreprimus.cli import app


def _write_template(path: Path, records: list[dict[str, object]]) -> None:
    path.write_text(yaml.safe_dump({"records": records}, sort_keys=False), encoding="utf-8")


def _record(case_id: str, index: int, token: str, notes: str) -> dict[str, object]:
    return {
        "challenge_id": case_id,
        "token_index_0_based": index,
        "canonical_token": token,
        "reviewer_notes": notes,
    }


def test_stage5bo_cli_validate_and_summary_work() -> None:
    runner = CliRunner()

    validate_result = runner.invoke(app, ["token-block", "validate-stage5bo"])
    assert validate_result.exit_code == 0, validate_result.output
    assert "token_block_stage5bo_valid=true" in validate_result.output
    assert "string4_branch_membership_status_after_errata=full_branch_match" in validate_result.output

    summary_result = runner.invoke(app, ["token-block", "stage5bo-summary"])
    assert summary_result.exit_code == 0, summary_result.output
    assert "stage5bn_addendum_integrated_as_inactive=true" in summary_result.output


def test_stage5bo_cli_build_is_ci_safe_with_synthetic_templates(tmp_path: Path) -> None:
    original = tmp_path / "decision-template.yaml"
    corrected = tmp_path / "decision-template-corrected.yaml"
    out = tmp_path / "records"
    results = tmp_path / "results"
    _write_template(
        original,
        [
            _record("stage5at-token-case-198", 198, "1j", "reviewed; possible_tokens=1I|1j"),
            _record("stage5at-token-case-199", 199, "0I", "reviewed; possible_tokens=0I|0j|OI|Oj"),
        ],
    )
    _write_template(
        corrected,
        [
            _record("stage5at-token-case-198", 198, "1j", "reviewed; possible_tokens=1i|1j"),
            _record("stage5at-token-case-199", 199, "0I", "reviewed; possible_tokens=0I|0l|OI|Ol"),
        ],
    )

    result = CliRunner().invoke(
        app,
        [
            "token-block",
            "build-stage5bo-decision-template-errata",
            "--original-template",
            str(original),
            "--corrected-template",
            str(corrected),
            "--results-dir",
            str(results),
            "--out-source-lock",
            str(out / "source-lock.yaml"),
            "--out-errata",
            str(out / "errata.yaml"),
            "--out-impact",
            str(out / "impact.yaml"),
            "--out-universe",
            str(out / "universe.yaml"),
            "--out-string4",
            str(out / "string4.yaml"),
            "--out-addendum-integration",
            str(out / "addendum.yaml"),
            "--out-gap-closure",
            str(out / "gap-closure.yaml"),
            "--out-planning-constraint",
            str(out / "planning.yaml"),
            "--out-lineage",
            str(out / "lineage.yaml"),
            "--out-future-impact",
            str(out / "future.yaml"),
            "--out-source-gap-severity",
            str(out / "gap-severity.yaml"),
            "--out-dwh",
            str(out / "dwh.yaml"),
            "--out-guardrail",
            str(out / "guardrail.yaml"),
            "--out-handoff",
            str(out / "handoff.yaml"),
            "--out-summary",
            str(out / "summary.yaml"),
            "--out-next-stage",
            str(out / "next-stage.yaml"),
        ],
    )

    assert result.exit_code == 0, result.output
    assert "token_case_errata_record_count=2" in result.output
    assert "case_199_operator_errata_found=true" in result.output
    assert "string4_branch_membership_status_after_errata=full_branch_match" in result.output
