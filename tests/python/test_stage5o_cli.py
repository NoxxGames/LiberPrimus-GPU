from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5o_cli_no_gpu_safe_round_trip(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage5o"
    repeat_run = tmp_path / "repeat-run.yaml"
    repeat_parity = tmp_path / "repeat-parity.yaml"
    result_store = tmp_path / "result-store.yaml"
    score = tmp_path / "score.yaml"
    decision = tmp_path / "decision.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()
    commands = [
        [
            "gematria-solved-fixture-cuda-repeat",
            "build-repeat-run-records",
            "--repeat-run-out",
            str(repeat_run),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-solved-fixture-cuda-repeat",
            "run-repeat-verification",
            "--repeat-run-records",
            str(repeat_run),
            "--repeat-run-out",
            str(repeat_run),
            "--out-dir",
            str(out_dir),
            "--skip-run",
            "--allow-warnings",
        ],
        [
            "gematria-solved-fixture-cuda-repeat",
            "build-repeat-parity-records",
            "--repeat-run-records",
            str(repeat_run),
            "--repeat-parity-out",
            str(repeat_parity),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-solved-fixture-cuda-repeat",
            "build-result-store-preflight",
            "--repeat-parity",
            str(repeat_parity),
            "--result-store-preflight-out",
            str(result_store),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-solved-fixture-cuda-repeat",
            "build-score-summary-preflight",
            "--repeat-parity",
            str(repeat_parity),
            "--score-summary-preflight-out",
            str(score),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-solved-fixture-cuda-repeat",
            "build-expansion-decision",
            "--repeat-parity",
            str(repeat_parity),
            "--result-store-preflight",
            str(result_store),
            "--score-summary-preflight",
            str(score),
            "--expansion-decision-out",
            str(decision),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-solved-fixture-cuda-repeat",
            "build-summary",
            "--repeat-run-records",
            str(repeat_run),
            "--repeat-parity-records",
            str(repeat_parity),
            "--result-store-preflight",
            str(result_store),
            "--score-summary-preflight",
            str(score),
            "--expansion-decision",
            str(decision),
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
            "gematria-solved-fixture-cuda-repeat",
            "validate-stage5o",
            "--repeat-run-records",
            str(repeat_run),
            "--repeat-parity-records",
            str(repeat_parity),
            "--result-store-preflight",
            str(result_store),
            "--score-summary-preflight",
            str(score),
            "--expansion-decision",
            str(decision),
            "--summary",
            str(summary),
            "--results-dir",
            str(out_dir),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "gematria_solved_fixture_cuda_repeat_stage5o_valid=true" in validate.output

    printed = runner.invoke(
        app,
        ["gematria-solved-fixture-cuda-repeat", "summary", "--summary", str(summary)],
    )
    assert printed.exit_code == 0, printed.output
    assert "repeat_cuda_skip_count=5" in printed.output
    assert "stage5p_ready=False" in printed.output


def test_stage5o_cli_existing_stage5n_command_still_registered() -> None:
    result = CliRunner().invoke(app, ["gematria-solved-fixture-cuda-reporting", "summary", "--help"])
    assert result.exit_code == 0, result.output
