from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.bounded_p56_cuda_parity.cli import app

runner = CliRunner()


def test_stage5ad_cli_builds_and_validates_skip_path(tmp_path: Path) -> None:
    out = tmp_path / "out"
    build = tmp_path / "build"
    run = tmp_path / "run.yaml"
    parity = tmp_path / "parity.yaml"
    result_store = tmp_path / "result.yaml"
    score_summary = tmp_path / "score.yaml"
    full = tmp_path / "full.yaml"
    scored = tmp_path / "scored.yaml"
    docs = tmp_path / "docs.yaml"
    audit = tmp_path / "audit.yaml"
    decision = tmp_path / "decision.yaml"
    summary = tmp_path / "summary.yaml"
    commands = [
        ["build-run-records", "--cuda-run-out", str(run), "--out-dir", str(out), "--allow-warnings"],
        [
            "run-bounded-p56-cuda",
            "--cuda-run-out",
            str(run),
            "--out-dir",
            str(out),
            "--build-dir",
            str(build),
            "--skip-cuda",
            "--allow-warnings",
        ],
        ["build-parity-records", "--cuda-run", str(run), "--cuda-parity-out", str(parity), "--out-dir", str(out), "--allow-warnings"],
        [
            "build-result-store-preflight",
            "--cuda-parity",
            str(parity),
            "--result-store-preflight-out",
            str(result_store),
            "--out-dir",
            str(out),
            "--allow-warnings",
        ],
        [
            "build-score-summary-preflight",
            "--cuda-parity",
            str(parity),
            "--score-summary-preflight-out",
            str(score_summary),
            "--out-dir",
            str(out),
            "--allow-warnings",
        ],
        ["build-full-p56-blocker", "--full-p56-blocker-out", str(full), "--out-dir", str(out), "--allow-warnings"],
        ["build-scored-experiment-deferral", "--scored-experiment-deferral-out", str(scored), "--out-dir", str(out), "--allow-warnings"],
        ["build-doc-staleness-validation", "--doc-staleness-validation-out", str(docs), "--out-dir", str(out), "--allow-warnings"],
        ["build-device-subset-audit", "--device-subset-audit-out", str(audit), "--out-dir", str(out), "--allow-warnings"],
        [
            "build-next-stage-decision",
            "--cuda-parity",
            str(parity),
            "--next-stage-decision-out",
            str(decision),
            "--out-dir",
            str(out),
            "--allow-warnings",
        ],
        [
            "build-summary",
            "--cuda-run",
            str(run),
            "--cuda-parity",
            str(parity),
            "--result-store-preflight",
            str(result_store),
            "--score-summary-preflight",
            str(score_summary),
            "--full-p56-blocker",
            str(full),
            "--scored-experiment-deferral",
            str(scored),
            "--doc-staleness-validation",
            str(docs),
            "--device-subset-audit",
            str(audit),
            "--next-stage-decision",
            str(decision),
            "--summary-out",
            str(summary),
            "--out-dir",
            str(out),
            "--allow-warnings",
        ],
        [
            "validate-stage5ad",
            "--cuda-run",
            str(run),
            "--cuda-parity",
            str(parity),
            "--result-store-preflight",
            str(result_store),
            "--score-summary-preflight",
            str(score_summary),
            "--full-p56-blocker",
            str(full),
            "--scored-experiment-deferral",
            str(scored),
            "--doc-staleness-validation",
            str(docs),
            "--device-subset-audit",
            str(audit),
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
    assert "stage5ad_parity_status=skipped_cuda_unavailable" in summary_result.output
    assert "Stage 5AD-followup" in summary_result.output
    assert "bounded p56 CUDA toolchain" in summary_result.output
