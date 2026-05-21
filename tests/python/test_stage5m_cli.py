from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5m_cli_no_gpu_safe_round_trip(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage5m"
    run_records = tmp_path / "run.yaml"
    parity_records = tmp_path / "parity.yaml"
    boundaries = tmp_path / "boundaries.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()

    commands = [
        [
            "gematria-solved-fixture-cuda",
            "build-run-records",
            "--run-records-out",
            str(run_records),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-solved-fixture-cuda",
            "run-cuda-parity",
            "--run-records",
            str(run_records),
            "--run-records-out",
            str(run_records),
            "--out-dir",
            str(out_dir),
            "--skip-run",
            "--allow-warnings",
        ],
        [
            "gematria-solved-fixture-cuda",
            "build-parity-records",
            "--run-records",
            str(run_records),
            "--parity-records-out",
            str(parity_records),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-solved-fixture-cuda",
            "build-boundary-records",
            "--run-records",
            str(run_records),
            "--boundaries-out",
            str(boundaries),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-solved-fixture-cuda",
            "build-summary",
            "--run-records",
            str(run_records),
            "--parity-records",
            str(parity_records),
            "--boundaries",
            str(boundaries),
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
            "gematria-solved-fixture-cuda",
            "validate-stage5m",
            "--run-records",
            str(run_records),
            "--parity-records",
            str(parity_records),
            "--boundaries",
            str(boundaries),
            "--summary",
            str(summary),
            "--results-dir",
            str(out_dir),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "gematria_solved_fixture_cuda_stage5m_valid=true" in validate.output

    printed = runner.invoke(app, ["gematria-solved-fixture-cuda", "summary", "--summary", str(summary)])
    assert printed.exit_code == 0, printed.output
    assert "stage5n_ready=False" in printed.output
    assert "cuda_skip_count=5" in printed.output
