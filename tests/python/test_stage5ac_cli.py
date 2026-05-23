from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.prime_minus_one_cuda_synthetic_reporting.cli import app

runner = CliRunner()


def test_stage5ac_cli_builds_and_validates_tmp_records(tmp_path: Path) -> None:
    out = tmp_path / "out"
    parity = tmp_path / "parity.yaml"
    result_store = tmp_path / "result.yaml"
    score_summary = tmp_path / "score.yaml"
    method_status = tmp_path / "method.yaml"
    generated_body = tmp_path / "body.yaml"
    bounded = tmp_path / "bounded.yaml"
    full = tmp_path / "full.yaml"
    scored = tmp_path / "scored.yaml"
    docs = tmp_path / "docs.yaml"
    decision = tmp_path / "decision.yaml"
    summary = tmp_path / "summary.yaml"
    commands = [
        ["build-parity-report", "--parity-report-out", str(parity), "--out-dir", str(out), "--allow-warnings"],
        [
            "build-result-store-integration",
            "--parity-report",
            str(parity),
            "--result-store-integration-out",
            str(result_store),
            "--out-dir",
            str(out),
            "--allow-warnings",
        ],
        [
            "build-score-summary-integration",
            "--parity-report",
            str(parity),
            "--score-summary-integration-out",
            str(score_summary),
            "--out-dir",
            str(out),
            "--allow-warnings",
        ],
        ["build-method-status-impact", "--method-status-impact-out", str(method_status), "--out-dir", str(out), "--allow-warnings"],
        ["build-generated-body-policy", "--generated-body-policy-out", str(generated_body), "--out-dir", str(out), "--allow-warnings"],
        ["build-doc-staleness-validation", "--doc-staleness-validation-out", str(docs), "--out-dir", str(out), "--allow-warnings"],
        [
            "build-bounded-p56-preflight",
            "--parity-report",
            str(parity),
            "--doc-staleness-validation",
            str(docs),
            "--bounded-p56-preflight-out",
            str(bounded),
            "--out-dir",
            str(out),
            "--allow-warnings",
        ],
        ["build-full-p56-blocker", "--full-p56-blocker-out", str(full), "--out-dir", str(out), "--allow-warnings"],
        ["build-scored-experiment-deferral", "--scored-experiment-deferral-out", str(scored), "--out-dir", str(out), "--allow-warnings"],
        [
            "build-next-stage-decision",
            "--parity-report",
            str(parity),
            "--bounded-p56-preflight",
            str(bounded),
            "--doc-staleness-validation",
            str(docs),
            "--next-stage-decision-out",
            str(decision),
            "--out-dir",
            str(out),
            "--allow-warnings",
        ],
        [
            "build-summary",
            "--parity-report",
            str(parity),
            "--result-store-integration",
            str(result_store),
            "--score-summary-integration",
            str(score_summary),
            "--method-status-impact",
            str(method_status),
            "--generated-body-policy",
            str(generated_body),
            "--bounded-p56-preflight",
            str(bounded),
            "--full-p56-blocker",
            str(full),
            "--scored-experiment-deferral",
            str(scored),
            "--doc-staleness-validation",
            str(docs),
            "--next-stage-decision",
            str(decision),
            "--summary-out",
            str(summary),
            "--out-dir",
            str(out),
            "--allow-warnings",
        ],
        [
            "validate-stage5ac",
            "--parity-report",
            str(parity),
            "--result-store-integration",
            str(result_store),
            "--score-summary-integration",
            str(score_summary),
            "--method-status-impact",
            str(method_status),
            "--generated-body-policy",
            str(generated_body),
            "--bounded-p56-preflight",
            str(bounded),
            "--full-p56-blocker",
            str(full),
            "--scored-experiment-deferral",
            str(scored),
            "--doc-staleness-validation",
            str(docs),
            "--next-stage-decision",
            str(decision),
            "--summary",
            str(summary),
            "--results-dir",
            str(out),
        ],
    ]
    for command in commands:
        result = runner.invoke(app, command)
        assert result.exit_code == 0, result.output
    summary_result = runner.invoke(app, ["summary", "--summary", str(summary)])
    assert summary_result.exit_code == 0
    assert "Stage 5AD - bounded p56 CUDA parity run" in summary_result.output
