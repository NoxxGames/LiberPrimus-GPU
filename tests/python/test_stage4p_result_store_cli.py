from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


SOURCE_MANIFEST = "experiments/manifests/result-store/stage4p-result-source-inventory.yaml"
SCORE_MANIFEST = "experiments/manifests/result-store/stage4p-score-summary-unification.yaml"
REPORT_MANIFEST = "experiments/manifests/result-store/stage4p-cross-stage-report.yaml"
STAGE2B_MANIFEST = "experiments/manifests/result-store/stage2b-solved-baseline-import.yaml"


def test_stage4p_result_store_cli_commands(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage4p"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()

    inventory = runner.invoke(
        app,
        ["result-store", "build-source-inventory", "--manifest", SOURCE_MANIFEST, "--out-dir", str(out_dir), "--allow-warnings"],
    )
    assert inventory.exit_code == 0, inventory.output
    assert "source_inventory_records=" in inventory.output

    scores = runner.invoke(
        app,
        ["result-store", "unify-score-summaries", "--manifest", SCORE_MANIFEST, "--out-dir", str(out_dir), "--allow-warnings"],
    )
    assert scores.exit_code == 0, scores.output
    assert "unified_score_summary_records=" in scores.output

    report = runner.invoke(
        app,
        [
            "result-store",
            "build-cross-stage-report",
            "--manifest",
            REPORT_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--summary-out",
            str(summary),
            "--allow-warnings",
        ],
    )
    assert report.exit_code == 0, report.output
    assert "cross_stage_report_written=true" in report.output

    validate = runner.invoke(
        app,
        ["result-store", "validate-stage4p", "--results-dir", str(out_dir), "--summary", str(summary)],
    )
    assert validate.exit_code == 0, validate.output
    assert "result_store_stage4p_valid=true" in validate.output


def test_existing_result_store_validate_manifest_still_works() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["result-store", "validate-manifest", "--manifest", STAGE2B_MANIFEST])
    assert result.exit_code == 0, result.output
    assert "Result-store manifest validation OK" in result.output
