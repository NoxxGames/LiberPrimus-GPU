from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage4i_scoring_cli_consolidate_validate_report(tmp_path: Path) -> None:
    data_dir = tmp_path / "scoring"
    out_dir = tmp_path / "out"
    runner = CliRunner()

    consolidate = runner.invoke(
        app,
        [
            "scoring",
            "consolidate",
            "--out-dir",
            str(out_dir),
            "--data-dir",
            str(data_dir),
            "--allow-warnings",
        ],
    )
    assert consolidate.exit_code == 0, consolidate.output
    assert "scorer_record_count=3" in consolidate.output

    validate = runner.invoke(app, ["scoring", "validate", "--data-dir", str(data_dir)])
    assert validate.exit_code == 0, validate.output
    assert "scoring_records_valid=true" in validate.output

    report = runner.invoke(app, ["scoring", "report", "--data-dir", str(data_dir)])
    assert report.exit_code == 0, report.output
    assert "confidence_label_count=9" in report.output

    compatibility = runner.invoke(
        app,
        [
            "scoring",
            "check-cpu-batch-compatibility",
            "--cpu-batch-summary",
            "data/research/stage4h-cpu-batch-api-summary.yaml",
            "--data-dir",
            str(data_dir),
            "--allow-warnings",
        ],
    )
    assert compatibility.exit_code == 0, compatibility.output
    assert "compatible=true" in compatibility.output
