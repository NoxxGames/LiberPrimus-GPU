from __future__ import annotations

import json
from pathlib import Path

import yaml
from typer.testing import CliRunner

from libreprimus.cli import app
from libreprimus.doc_staleness.stage_ledger import stage_ledger_findings_for_text


def _write_required_generated_reports(out_dir: Path) -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    findings = [
        finding.to_dict()
        for finding in stage_ledger_findings_for_text(
            readme,
            path="README.md",
            expected_latest_stage="Stage 5AH",
        )
    ]
    (out_dir / "readme_stage_coverage_report.json").write_text(
        json.dumps(
            {
                "record_type": "readme_stage_coverage_report",
                "expected_latest_stage": "Stage 5AH",
                "finding_count": len(findings),
                "findings": findings,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    summary = yaml.safe_load(
        Path("data/project-state/stage5ah-doc-staleness-summary.yaml").read_text(encoding="utf-8")
    )
    (out_dir / "doc_staleness_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out_dir / "warnings.jsonl").write_text("", encoding="utf-8")


def test_stage5ah_cli_commands_write_reports_and_validate(tmp_path: Path) -> None:
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "consistency",
            "check-stage-ledger-staleness",
            "--expected-latest-stage",
            "Stage 5AH",
            "--expected-next-stage",
            "Stage 5AI",
            "--out",
            str(tmp_path / "stale_stage_ledger_report.json"),
        ],
    )
    assert result.exit_code == 0, result.output

    result = runner.invoke(
        app,
        [
            "consistency",
            "check-operational-file-map-coverage",
            "--out",
            str(tmp_path / "operational_file_map_coverage_report.json"),
        ],
    )
    assert result.exit_code == 0, result.output

    result = runner.invoke(
        app,
        [
            "consistency",
            "check-current-next-stage-consistency",
            "--expected-latest-stage",
            "Stage 5AH",
            "--expected-next-stage",
            "Stage 5AI",
            "--out",
            str(tmp_path / "current_next_stage_report.json"),
        ],
    )
    assert result.exit_code == 0, result.output

    _write_required_generated_reports(tmp_path)
    result = runner.invoke(
        app,
        [
            "consistency",
            "validate-stage5ah-doc-staleness",
            "--source-of-truth",
            "data/project-state/stage5ah-doc-staleness-source-of-truth.yaml",
            "--findings",
            "data/project-state/stage5ah-doc-staleness-findings.yaml",
            "--stage-ledger-coverage",
            "data/project-state/stage5ah-stage-ledger-coverage.yaml",
            "--operational-file-map-coverage",
            "data/project-state/stage5ah-operational-file-map-coverage.yaml",
            "--next-stage-decision",
            "data/project-state/stage5ah-next-stage-decision.yaml",
            "--summary",
            "data/project-state/stage5ah-doc-staleness-summary.yaml",
            "--results-dir",
            str(tmp_path),
        ],
    )
    assert result.exit_code == 0, result.output
    assert "stage5ah_doc_staleness_valid=true" in result.output
