from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5s_cli_round_trip_no_cuda_execution(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage5s"
    parity = tmp_path / "parity.yaml"
    result_store = tmp_path / "result-store.yaml"
    score = tmp_path / "score.yaml"
    method = tmp_path / "method.yaml"
    policy = tmp_path / "policy.yaml"
    boundary = tmp_path / "boundary.yaml"
    decision = tmp_path / "decision.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()
    commands = [
        [
            "gematria-expanded-cuda-result-store",
            "build-parity-report",
            "--parity-report-out",
            str(parity),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-expanded-cuda-result-store",
            "build-result-store-integration",
            "--parity-report",
            str(parity),
            "--result-store-integration-out",
            str(result_store),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-expanded-cuda-result-store",
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
            "gematria-expanded-cuda-result-store",
            "build-method-status-impact",
            "--method-status-impact-out",
            str(method),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-expanded-cuda-result-store",
            "build-generated-body-policy",
            "--generated-body-policy-out",
            str(policy),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-expanded-cuda-result-store",
            "build-boundary-review",
            "--boundary-review-out",
            str(boundary),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-expanded-cuda-result-store",
            "build-next-step-decision",
            "--next-step-decision-out",
            str(decision),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-expanded-cuda-result-store",
            "build-summary",
            "--parity-report",
            str(parity),
            "--result-store-integration",
            str(result_store),
            "--score-summary-integration",
            str(score),
            "--method-status-impact",
            str(method),
            "--generated-body-policy",
            str(policy),
            "--boundary-review",
            str(boundary),
            "--next-step-decision",
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
            "gematria-expanded-cuda-result-store",
            "validate-stage5s",
            "--parity-report",
            str(parity),
            "--result-store-integration",
            str(result_store),
            "--score-summary-integration",
            str(score),
            "--method-status-impact",
            str(method),
            "--generated-body-policy",
            str(policy),
            "--boundary-review",
            str(boundary),
            "--next-step-decision",
            str(decision),
            "--summary",
            str(summary),
            "--results-dir",
            str(out_dir),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "gematria_expanded_cuda_result_store_stage5s_valid=true" in validate.output

    printed = runner.invoke(
        app,
        ["gematria-expanded-cuda-result-store", "summary", "--summary", str(summary)],
    )
    assert printed.exit_code == 0, printed.output
    assert "cuda_execution_performed=False" in printed.output
    assert "deep_research_recommended=True" in printed.output


def test_stage5s_cli_keeps_stage5r_command_registered() -> None:
    result = CliRunner().invoke(app, ["gematria-expanded-solved-fixture-cuda", "summary", "--help"])
    assert result.exit_code == 0, result.output
