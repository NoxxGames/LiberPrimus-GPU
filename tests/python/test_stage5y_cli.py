from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5y_cli_build_validate_and_summary(tmp_path: Path) -> None:
    runner = CliRunner()
    paths = {
        "parity": tmp_path / "parity.yaml",
        "result": tmp_path / "result.yaml",
        "score": tmp_path / "score.yaml",
        "method": tmp_path / "method.yaml",
        "policy": tmp_path / "policy.yaml",
        "blocker": tmp_path / "blocker.yaml",
        "gate": tmp_path / "gate.yaml",
        "scored": tmp_path / "scored.yaml",
        "guardrail": tmp_path / "guardrail.yaml",
        "decision": tmp_path / "decision.yaml",
        "summary": tmp_path / "summary.yaml",
    }
    commands = [
        ["prime-minus-one-native-reporting", "build-parity-report", "--parity-report-out", str(paths["parity"]), "--out-dir", str(tmp_path), "--allow-warnings"],
        [
            "prime-minus-one-native-reporting",
            "build-result-store-integration",
            "--parity-report",
            str(paths["parity"]),
            "--result-store-integration-out",
            str(paths["result"]),
            "--out-dir",
            str(tmp_path),
            "--allow-warnings",
        ],
        [
            "prime-minus-one-native-reporting",
            "build-score-summary-integration",
            "--parity-report",
            str(paths["parity"]),
            "--score-summary-integration-out",
            str(paths["score"]),
            "--out-dir",
            str(tmp_path),
            "--allow-warnings",
        ],
        ["prime-minus-one-native-reporting", "build-method-status-impact", "--method-status-impact-out", str(paths["method"]), "--out-dir", str(tmp_path), "--allow-warnings"],
        ["prime-minus-one-native-reporting", "build-generated-body-policy", "--generated-body-policy-out", str(paths["policy"]), "--out-dir", str(tmp_path), "--allow-warnings"],
        [
            "prime-minus-one-native-reporting",
            "build-full-p56-blocker-preservation",
            "--full-p56-blocker-preservation-out",
            str(paths["blocker"]),
            "--out-dir",
            str(tmp_path),
            "--allow-warnings",
        ],
        [
            "prime-minus-one-native-reporting",
            "build-cuda-contract-readiness-gate",
            "--parity-report",
            str(paths["parity"]),
            "--result-store-integration",
            str(paths["result"]),
            "--score-summary-integration",
            str(paths["score"]),
            "--cuda-contract-readiness-gate-out",
            str(paths["gate"]),
            "--out-dir",
            str(tmp_path),
            "--allow-warnings",
        ],
        ["prime-minus-one-native-reporting", "build-scored-experiment-readiness", "--scored-experiment-readiness-out", str(paths["scored"]), "--out-dir", str(tmp_path), "--allow-warnings"],
        ["prime-minus-one-native-reporting", "build-guardrails", "--guardrail-out", str(paths["guardrail"]), "--out-dir", str(tmp_path), "--allow-warnings"],
        [
            "prime-minus-one-native-reporting",
            "build-next-stage-decision",
            "--cuda-contract-readiness-gate",
            str(paths["gate"]),
            "--next-stage-decision-out",
            str(paths["decision"]),
            "--out-dir",
            str(tmp_path),
            "--allow-warnings",
        ],
    ]
    for command in commands:
        result = runner.invoke(app, command)
        assert result.exit_code == 0, result.output

    summary_command = [
        "prime-minus-one-native-reporting",
        "build-summary",
        "--parity-report",
        str(paths["parity"]),
        "--result-store-integration",
        str(paths["result"]),
        "--score-summary-integration",
        str(paths["score"]),
        "--method-status-impact",
        str(paths["method"]),
        "--generated-body-policy",
        str(paths["policy"]),
        "--full-p56-blocker-preservation",
        str(paths["blocker"]),
        "--cuda-contract-readiness-gate",
        str(paths["gate"]),
        "--scored-experiment-readiness",
        str(paths["scored"]),
        "--guardrail",
        str(paths["guardrail"]),
        "--next-stage-decision",
        str(paths["decision"]),
        "--summary-out",
        str(paths["summary"]),
        "--out-dir",
        str(tmp_path),
        "--allow-warnings",
    ]
    assert runner.invoke(app, summary_command).exit_code == 0

    validation = runner.invoke(
        app,
        [
            "prime-minus-one-native-reporting",
            "validate-stage5y",
            "--parity-report",
            str(paths["parity"]),
            "--result-store-integration",
            str(paths["result"]),
            "--score-summary-integration",
            str(paths["score"]),
            "--method-status-impact",
            str(paths["method"]),
            "--generated-body-policy",
            str(paths["policy"]),
            "--full-p56-blocker-preservation",
            str(paths["blocker"]),
            "--cuda-contract-readiness-gate",
            str(paths["gate"]),
            "--scored-experiment-readiness",
            str(paths["scored"]),
            "--guardrail",
            str(paths["guardrail"]),
            "--next-stage-decision",
            str(paths["decision"]),
            "--summary",
            str(paths["summary"]),
            "--results-dir",
            str(tmp_path),
        ],
    )
    assert validation.exit_code == 0, validation.output
    assert "prime_minus_one_native_reporting_stage5y_valid=true" in validation.output

    summary = runner.invoke(app, ["prime-minus-one-native-reporting", "summary", "--summary", str(paths["summary"])])
    assert summary.exit_code == 0, summary.output
    assert "Stage 5Z - prime-minus-one CUDA contract" in summary.output
    assert "preparation" in summary.output
