from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app
from test_stage2b_import_solved_baseline_synthetic import write_synthetic_solved_baseline


def test_result_store_cli_manifest_import_validate_summary(tmp_path: Path) -> None:
    manifest, solved_dir, out_dir = write_synthetic_solved_baseline(tmp_path)
    runner = CliRunner()

    validate_manifest = runner.invoke(app, ["result-store", "validate-manifest", "--manifest", str(manifest)])
    imported = runner.invoke(
        app,
        [
            "result-store",
            "import-solved-baseline",
            "--manifest",
            str(manifest),
            "--solved-baseline-results",
            str(solved_dir),
            "--out-dir",
            str(out_dir),
            "--replace",
            "--allow-warnings",
        ],
    )
    validated = runner.invoke(
        app,
        [
            "result-store",
            "validate",
            "--results-dir",
            str(out_dir),
            "--sqlite",
            str(out_dir / "results.sqlite3"),
        ],
    )
    summary = runner.invoke(app, ["result-store", "summary", "--results-dir", str(out_dir)])

    assert validate_manifest.exit_code == 0, validate_manifest.output
    assert imported.exit_code == 0, imported.output
    assert "run_count=1" in imported.output
    assert validated.exit_code == 0, validated.output
    assert summary.exit_code == 0, summary.output
    assert "pass_count=1" in summary.output


def test_result_store_cli_missing_input_returns_nonzero(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        ["result-store", "validate-manifest", "--manifest", str(tmp_path / "missing.yaml")],
    )

    assert result.exit_code != 0
    assert "not found" in result.output.lower()


def test_result_store_import_missing_solved_outputs_returns_nonzero(tmp_path: Path) -> None:
    manifest, _, out_dir = write_synthetic_solved_baseline(tmp_path)
    result = CliRunner().invoke(
        app,
        [
            "result-store",
            "import-solved-baseline",
            "--manifest",
            str(manifest),
            "--solved-baseline-results",
            str(tmp_path / "missing"),
            "--out-dir",
            str(out_dir),
        ],
    )

    assert result.exit_code != 0
    assert "missing" in result.output.lower()
