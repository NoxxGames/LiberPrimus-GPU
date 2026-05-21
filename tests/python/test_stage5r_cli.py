from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5r_cli_round_trip_no_gpu_skip(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage5r"
    run_records = tmp_path / "run.yaml"
    parity_records = tmp_path / "parity.yaml"
    boundaries = tmp_path / "boundaries.yaml"
    result_store = tmp_path / "result-store.yaml"
    score_summary = tmp_path / "score-summary.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()
    commands = [
        [
            "gematria-expanded-solved-fixture-cuda",
            "build-run-records",
            "--run-records-out",
            str(run_records),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-expanded-solved-fixture-cuda",
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
            "gematria-expanded-solved-fixture-cuda",
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
            "gematria-expanded-solved-fixture-cuda",
            "build-boundary-records",
            "--run-records",
            str(run_records),
            "--parity-records",
            str(parity_records),
            "--boundaries-out",
            str(boundaries),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-expanded-solved-fixture-cuda",
            "build-result-store-preflight",
            "--parity-records",
            str(parity_records),
            "--result-store-preflight-out",
            str(result_store),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-expanded-solved-fixture-cuda",
            "build-score-summary-preflight",
            "--parity-records",
            str(parity_records),
            "--score-summary-preflight-out",
            str(score_summary),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-expanded-solved-fixture-cuda",
            "build-summary",
            "--run-records",
            str(run_records),
            "--parity-records",
            str(parity_records),
            "--boundaries",
            str(boundaries),
            "--result-store-preflight",
            str(result_store),
            "--score-summary-preflight",
            str(score_summary),
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
            "gematria-expanded-solved-fixture-cuda",
            "validate-stage5r",
            "--run-records",
            str(run_records),
            "--parity-records",
            str(parity_records),
            "--boundaries",
            str(boundaries),
            "--result-store-preflight",
            str(result_store),
            "--score-summary-preflight",
            str(score_summary),
            "--summary",
            str(summary),
            "--results-dir",
            str(out_dir),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "stage5s_ready=false" in validate.output


def test_stage5r_cli_keeps_stage5q_command_registered() -> None:
    result = CliRunner().invoke(app, ["gematria-expansion-candidate-mapping", "summary", "--help"])
    assert result.exit_code == 0, result.output
