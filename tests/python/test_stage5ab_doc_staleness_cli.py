from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5ab_doc_staleness_cli_strict_text() -> None:
    result = CliRunner().invoke(
        app,
        [
            "consistency",
            "check-doc-staleness",
            "--source-of-truth",
            "data/project-state/stage5ab-doc-staleness-source-of-truth.yaml",
            "--strict",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "doc_staleness_findings=0" in result.output


def test_stage5ab_doc_staleness_cli_json() -> None:
    result = CliRunner().invoke(
        app,
        [
            "consistency",
            "check-doc-staleness",
            "--source-of-truth",
            "data/project-state/stage5ab-doc-staleness-source-of-truth.yaml",
            "--format",
            "json",
        ],
    )

    assert result.exit_code == 0, result.output
    assert json.loads(result.output.split("doc_staleness_valid=true")[0])["summary"]["finding_count"] == 0


def test_stage5ab_doc_staleness_cli_write_report(tmp_path: Path) -> None:
    report = tmp_path / "staleness_findings.json"
    result = CliRunner().invoke(
        app,
        [
            "consistency",
            "check-doc-staleness",
            "--source-of-truth",
            "data/project-state/stage5ab-doc-staleness-source-of-truth.yaml",
            "--write-report",
            str(report),
        ],
    )

    assert result.exit_code == 0, result.output
    assert report.is_file()
    assert (report.parent / "summary.json").is_file()
    assert json.loads(report.read_text(encoding="utf-8"))["summary"]["finding_count"] == 0
