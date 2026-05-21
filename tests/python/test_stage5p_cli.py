from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5p_cli_round_trip(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage5p"
    result_store = tmp_path / "result-store.yaml"
    score = tmp_path / "score.yaml"
    method = tmp_path / "method.yaml"
    policy = tmp_path / "policy.yaml"
    candidates = tmp_path / "candidates.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()
    commands = [
        [
            "gematria-cuda-result-store",
            "build-result-store-integration",
            "--result-store-integration-out",
            str(result_store),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-cuda-result-store",
            "build-score-summary-integration",
            "--result-store-integration",
            str(result_store),
            "--score-summary-integration-out",
            str(score),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-cuda-result-store",
            "build-method-status-impact",
            "--result-store-integration",
            str(result_store),
            "--method-status-impact-out",
            str(method),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-cuda-result-store",
            "build-generated-body-policy",
            "--generated-body-policy-out",
            str(policy),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-cuda-result-store",
            "build-controlled-expansion-candidates",
            "--controlled-expansion-candidates-out",
            str(candidates),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-cuda-result-store",
            "build-summary",
            "--result-store-integration",
            str(result_store),
            "--score-summary-integration",
            str(score),
            "--method-status-impact",
            str(method),
            "--generated-body-policy",
            str(policy),
            "--controlled-expansion-candidates",
            str(candidates),
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
            "gematria-cuda-result-store",
            "validate-stage5p",
            "--result-store-integration",
            str(result_store),
            "--score-summary-integration",
            str(score),
            "--method-status-impact",
            str(method),
            "--generated-body-policy",
            str(policy),
            "--controlled-expansion-candidates",
            str(candidates),
            "--summary",
            str(summary),
            "--results-dir",
            str(out_dir),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "gematria_cuda_result_store_stage5p_valid=true" in validate.output

    printed = runner.invoke(app, ["gematria-cuda-result-store", "summary", "--summary", str(summary)])
    assert printed.exit_code == 0, printed.output
    assert "cuda_execution_performed=False" in printed.output


def test_stage5p_cli_keeps_stage5o_command_registered() -> None:
    result = CliRunner().invoke(app, ["gematria-solved-fixture-cuda-repeat", "summary", "--help"])
    assert result.exit_code == 0, result.output
