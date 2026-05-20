from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


SOLVED_MANIFEST = "experiments/manifests/cpu-batch/stage4o-solved-fixture-parity-batch.yaml"
COVERAGE_MANIFEST = "experiments/manifests/cpu-batch/stage4o-adapter-expansion-smoke-batch.yaml"
PARITY_MANIFEST = "experiments/manifests/cpu-batch/stage4o-cpu-cuda-parity-readiness.yaml"
STAGE4H_MANIFEST = "experiments/manifests/cpu-batch/stage4h-synthetic-smoke-batch.yaml"


def test_stage4o_cpu_batch_cli_commands(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage4o"
    summary = tmp_path / "stage4o-summary.yaml"
    runner = CliRunner()

    solved = runner.invoke(
        app,
        [
            "cpu-batch",
            "solved-fixture-parity",
            "--manifest",
            SOLVED_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    )
    assert solved.exit_code == 0, solved.output
    assert "executed_candidate_count=8" in solved.output

    coverage = runner.invoke(
        app,
        [
            "cpu-batch",
            "adapter-expansion",
            "--manifest",
            COVERAGE_MANIFEST,
            "--registry",
            "data/transform-registry/cpu-reference-transforms-v0.json",
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    )
    assert coverage.exit_code == 0, coverage.output
    assert "supported_adapter_count=9" in coverage.output

    parity = runner.invoke(
        app,
        [
            "cpu-batch",
            "parity-readiness",
            "--manifest",
            PARITY_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--summary-out",
            str(summary),
            "--allow-warnings",
        ],
    )
    assert parity.exit_code == 0, parity.output
    assert "parity_expectations_written=8" in parity.output

    validate = runner.invoke(app, ["cpu-batch", "validate-stage4o", "--results-dir", str(out_dir), "--summary", str(summary)])
    assert validate.exit_code == 0, validate.output
    assert "cpu_batch_stage4o_valid=true" in validate.output


def test_stage4o_stage4h_commands_still_work(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage4h"
    runner = CliRunner()
    run = runner.invoke(app, ["cpu-batch", "run", "--manifest", STAGE4H_MANIFEST, "--out-dir", str(out_dir), "--allow-warnings"])
    assert run.exit_code == 0, run.output
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
    validate = runner.invoke(app, ["cpu-batch", "validate-results", "--results-dir", str(out_dir)])
    assert validate.exit_code == 0, validate.output
