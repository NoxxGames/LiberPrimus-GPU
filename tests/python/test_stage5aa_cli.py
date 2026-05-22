from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.prime_minus_one_cuda_synthetic.cli import app

runner = CliRunner()


def test_stage5aa_cli_builds_and_validates_skip_path(tmp_path: Path) -> None:
    out = tmp_path / "out"
    kernel = tmp_path / "kernel.yaml"
    run = tmp_path / "run.yaml"
    parity = tmp_path / "parity.yaml"
    audit = tmp_path / "audit.yaml"
    result = tmp_path / "result.yaml"
    p56 = tmp_path / "p56.yaml"
    scored = tmp_path / "scored.yaml"
    decision = tmp_path / "decision.yaml"
    summary = tmp_path / "summary.yaml"
    commands = [
        ["build-kernel-implementation-records", "--kernel-implementation-out", str(kernel), "--out-dir", str(out)],
        ["run-synthetic-cuda-parity", "--cuda-run-out", str(run), "--out-dir", str(out), "--skip-cuda"],
        ["build-parity-records", "--cuda-run", str(run), "--parity-out", str(parity), "--out-dir", str(out)],
        ["build-device-subset-audit", "--device-subset-audit-out", str(audit), "--out-dir", str(out)],
        ["build-result-store-preflight", "--result-store-preflight-out", str(result), "--out-dir", str(out)],
        ["build-p56-blocker", "--p56-blocker-out", str(p56), "--out-dir", str(out)],
        ["build-scored-experiment-deferral", "--scored-experiment-deferral-out", str(scored), "--out-dir", str(out)],
        ["build-next-stage-decision", "--parity", str(parity), "--next-stage-decision-out", str(decision), "--out-dir", str(out)],
        [
            "build-summary",
            "--kernel-implementation",
            str(kernel),
            "--cuda-run",
            str(run),
            "--parity",
            str(parity),
            "--device-subset-audit",
            str(audit),
            "--result-store-preflight",
            str(result),
            "--p56-blocker",
            str(p56),
            "--scored-experiment-deferral",
            str(scored),
            "--next-stage-decision",
            str(decision),
            "--summary-out",
            str(summary),
            "--out-dir",
            str(out),
        ],
        [
            "validate-stage5aa",
            "--kernel-implementation",
            str(kernel),
            "--cuda-run",
            str(run),
            "--parity",
            str(parity),
            "--device-subset-audit",
            str(audit),
            "--result-store-preflight",
            str(result),
            "--p56-blocker",
            str(p56),
            "--scored-experiment-deferral",
            str(scored),
            "--next-stage-decision",
            str(decision),
            "--summary",
            str(summary),
            "--results-dir",
            str(out),
        ],
    ]
    for command in commands:
        result_obj = runner.invoke(app, command)
        assert result_obj.exit_code == 0, result_obj.output
    summary_obj = runner.invoke(app, ["summary", "--summary", str(summary)])
    assert summary_obj.exit_code == 0
    assert "parity_status=skipped_cuda_unavailable" in summary_obj.output
