from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


ENV_MANIFEST = "experiments/manifests/benchmarks/stage4q-benchmark-environment.yaml"
SMOKE_MANIFEST = "experiments/manifests/benchmarks/stage4q-cpu-benchmark-smoke.yaml"
READINESS_MANIFEST = "experiments/manifests/benchmarks/stage4q-cuda-parity-readiness.yaml"


def test_stage4q_benchmark_planning_cli(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage4q"
    plan = tmp_path / "plan.yaml"
    readiness = tmp_path / "readiness.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()

    environment = runner.invoke(
        app,
        ["benchmark-planning", "environment", "--manifest", ENV_MANIFEST, "--out-dir", str(out_dir), "--allow-warnings"],
    )
    assert environment.exit_code == 0, environment.output
    smoke = runner.invoke(
        app,
        ["benchmark-planning", "cpu-smoke", "--manifest", SMOKE_MANIFEST, "--out-dir", str(out_dir), "--allow-warnings"],
    )
    assert smoke.exit_code == 0, smoke.output
    build = runner.invoke(
        app,
        [
            "benchmark-planning",
            "build-plan",
            "--manifest",
            READINESS_MANIFEST,
            "--plan-out",
            str(plan),
            "--readiness-out",
            str(readiness),
            "--summary-out",
            str(summary),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    )
    assert build.exit_code == 0, build.output
    assert "future_cuda_targets_ready=9" in build.output
    validate = runner.invoke(
        app,
        [
            "benchmark-planning",
            "validate-stage4q",
            "--results-dir",
            str(out_dir),
            "--plan",
            str(plan),
            "--readiness",
            str(readiness),
            "--summary",
            str(summary),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "benchmark_planning_stage4q_valid=true" in validate.output
