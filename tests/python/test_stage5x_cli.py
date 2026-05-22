from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5x_cli_build_validate_and_summary(tmp_path: Path) -> None:
    runner = CliRunner()
    run = tmp_path / "run.yaml"
    parity = tmp_path / "parity.yaml"
    result = tmp_path / "result.yaml"
    score = tmp_path / "score.yaml"
    blocker = tmp_path / "blocker.yaml"
    guardrail = tmp_path / "guardrail.yaml"
    decision = tmp_path / "decision.yaml"
    summary = tmp_path / "summary.yaml"
    commands = [
        ["prime-minus-one-native-parity", "build-run-records", "--native-run-out", str(run), "--out-dir", str(tmp_path), "--allow-warnings"],
        ["prime-minus-one-native-parity", "run-native-parity", "--native-run-out", str(run), "--out-dir", str(tmp_path), "--allow-warnings"],
        ["prime-minus-one-native-parity", "build-parity-records", "--native-run", str(run), "--native-parity-out", str(parity), "--out-dir", str(tmp_path), "--allow-warnings"],
        ["prime-minus-one-native-parity", "build-result-store-preflight", "--native-parity", str(parity), "--result-store-preflight-out", str(result), "--out-dir", str(tmp_path), "--allow-warnings"],
        ["prime-minus-one-native-parity", "build-score-summary-preflight", "--native-parity", str(parity), "--score-summary-preflight-out", str(score), "--out-dir", str(tmp_path), "--allow-warnings"],
        ["prime-minus-one-native-parity", "build-full-p56-blocker", "--full-p56-blocker-out", str(blocker), "--out-dir", str(tmp_path), "--allow-warnings"],
        ["prime-minus-one-native-parity", "build-guardrails", "--guardrail-out", str(guardrail), "--out-dir", str(tmp_path), "--allow-warnings"],
        ["prime-minus-one-native-parity", "build-next-stage-decision", "--native-parity", str(parity), "--next-stage-decision-out", str(decision), "--out-dir", str(tmp_path), "--allow-warnings"],
        [
            "prime-minus-one-native-parity",
            "build-summary",
            "--native-run",
            str(run),
            "--native-parity",
            str(parity),
            "--result-store-preflight",
            str(result),
            "--score-summary-preflight",
            str(score),
            "--full-p56-blocker",
            str(blocker),
            "--guardrail",
            str(guardrail),
            "--next-stage-decision",
            str(decision),
            "--summary-out",
            str(summary),
            "--out-dir",
            str(tmp_path),
            "--allow-warnings",
        ],
    ]
    for command in commands:
        invocation = runner.invoke(app, command)
        assert invocation.exit_code == 0, invocation.output

    validation = runner.invoke(
        app,
        [
            "prime-minus-one-native-parity",
            "validate-stage5x",
            "--native-run",
            str(run),
            "--native-parity",
            str(parity),
            "--result-store-preflight",
            str(result),
            "--score-summary-preflight",
            str(score),
            "--full-p56-blocker",
            str(blocker),
            "--guardrail",
            str(guardrail),
            "--next-stage-decision",
            str(decision),
            "--summary",
            str(summary),
            "--results-dir",
            str(tmp_path),
        ],
    )
    assert validation.exit_code == 0, validation.output
    assert "prime_minus_one_native_parity_stage5x_valid=true" in validation.output

    summary_invocation = runner.invoke(app, ["prime-minus-one-native-parity", "summary", "--summary", str(summary)])
    assert summary_invocation.exit_code == 0, summary_invocation.output
    assert "native_pass_count=2" in summary_invocation.output
