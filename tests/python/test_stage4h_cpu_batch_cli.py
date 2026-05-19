from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


MANIFEST = "experiments/manifests/cpu-batch/stage4h-synthetic-smoke-batch.yaml"


def test_stage4h_cpu_batch_cli_run_validate_and_coverage(tmp_path: Path) -> None:
    out_dir = tmp_path / "cpu-batch"
    runner = CliRunner()

    validate = runner.invoke(app, ["cpu-batch", "validate-manifest", "--manifest", MANIFEST])
    assert validate.exit_code == 0, validate.output
    assert "cpu_batch_manifest_valid=true" in validate.output

    run = runner.invoke(
        app,
        [
            "cpu-batch",
            "run",
            "--manifest",
            MANIFEST,
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    )
    assert run.exit_code == 0, run.output
    assert "executed_candidate_count=6" in run.output

    coverage = runner.invoke(
        app,
        [
            "cpu-batch",
            "adapter-coverage",
            "--registry",
            "data/transform-registry/cpu-reference-transforms-v0.json",
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    )
    assert coverage.exit_code == 0, coverage.output
    assert "supported_adapter_count=6" in coverage.output

    result = runner.invoke(app, ["cpu-batch", "validate-results", "--results-dir", str(out_dir)])
    assert result.exit_code == 0, result.output
    assert "cpu_batch_results_valid=true" in result.output
