from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5n_cli_no_gpu_safe_round_trip(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage5n"
    parity = tmp_path / "parity.yaml"
    gates = tmp_path / "gates.yaml"
    boundary = tmp_path / "boundary.yaml"
    preflight = tmp_path / "preflight.yaml"
    guardrail = tmp_path / "guardrail.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()
    commands = [
        ["gematria-solved-fixture-cuda-reporting", "build-parity-report", "--parity-report-out", str(parity), "--out-dir", str(out_dir), "--allow-warnings"],
        ["gematria-solved-fixture-cuda-reporting", "build-controlled-expansion-gate", "--controlled-expansion-gate-out", str(gates), "--out-dir", str(out_dir), "--allow-warnings"],
        ["gematria-solved-fixture-cuda-reporting", "build-boundary-review", "--boundary-review-out", str(boundary), "--out-dir", str(out_dir), "--allow-warnings"],
        ["gematria-solved-fixture-cuda-reporting", "build-result-store-preflight", "--result-store-preflight-out", str(preflight), "--out-dir", str(out_dir), "--allow-warnings"],
        ["gematria-solved-fixture-cuda-reporting", "build-no-unsolved-guardrail", "--no-unsolved-guardrail-out", str(guardrail), "--out-dir", str(out_dir), "--allow-warnings"],
        [
            "gematria-solved-fixture-cuda-reporting",
            "build-summary",
            "--parity-report",
            str(parity),
            "--controlled-expansion-gate",
            str(gates),
            "--boundary-review",
            str(boundary),
            "--result-store-preflight",
            str(preflight),
            "--no-unsolved-guardrail",
            str(guardrail),
            "--summary-out",
            str(summary),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    ]
    for command in commands:
        result = runner.invoke(app, command)
        assert result.exit_code == 0, result.output

    validate = runner.invoke(
        app,
        [
            "gematria-solved-fixture-cuda-reporting",
            "validate-stage5n",
            "--parity-report",
            str(parity),
            "--controlled-expansion-gate",
            str(gates),
            "--boundary-review",
            str(boundary),
            "--result-store-preflight",
            str(preflight),
            "--no-unsolved-guardrail",
            str(guardrail),
            "--summary",
            str(summary),
            "--results-dir",
            str(out_dir),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "gematria_solved_fixture_cuda_reporting_stage5n_valid=true" in validate.output


def test_stage5n_summary_cli_reports_no_cuda_execution() -> None:
    result = CliRunner().invoke(
        app,
        [
            "gematria-solved-fixture-cuda-reporting",
            "summary",
            "--summary",
            "data/cuda/stage5n-solved-fixture-cuda-reporting-summary.yaml",
        ],
    )
    assert result.exit_code == 0, result.output
    assert "additional_cuda_execution_performed=False" in result.output
    assert "cuda_source_modified=False" in result.output
