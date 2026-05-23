from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.corrected_bounded_p56_reporting.cli import app

runner = CliRunner()


def test_stage5ae_cli_builds_and_validates(tmp_path: Path) -> None:
    out = tmp_path / "out"
    paths = {
        "formula": tmp_path / "formula.yaml",
        "contract": tmp_path / "contract.yaml",
        "policy": tmp_path / "policy.yaml",
        "result": tmp_path / "result.yaml",
        "score": tmp_path / "score.yaml",
        "method": tmp_path / "method.yaml",
        "body": tmp_path / "body.yaml",
        "full": tmp_path / "full.yaml",
        "scored": tmp_path / "scored.yaml",
        "archive": tmp_path / "archive.yaml",
        "docs": tmp_path / "docs.yaml",
        "decision": tmp_path / "decision.yaml",
        "summary": tmp_path / "summary.yaml",
    }
    commands = [
        ["build-formula-parity-report", "--formula-parity-report-out", str(paths["formula"]), "--out-dir", str(out), "--allow-warnings"],
        ["build-reference-contract-repair", "--reference-contract-repair-out", str(paths["contract"]), "--out-dir", str(out), "--allow-warnings"],
        ["build-hash-material-policy", "--hash-material-policy-out", str(paths["policy"]), "--out-dir", str(out), "--allow-warnings"],
        ["build-result-store-integration", "--result-store-integration-out", str(paths["result"]), "--out-dir", str(out), "--allow-warnings"],
        ["build-score-summary-integration", "--score-summary-integration-out", str(paths["score"]), "--out-dir", str(out), "--allow-warnings"],
        ["build-method-status-impact", "--method-status-impact-out", str(paths["method"]), "--out-dir", str(out), "--allow-warnings"],
        ["build-generated-body-policy", "--generated-body-policy-out", str(paths["body"]), "--out-dir", str(out), "--allow-warnings"],
        ["build-full-p56-blocker", "--full-p56-blocker-out", str(paths["full"]), "--out-dir", str(out), "--allow-warnings"],
        ["build-scored-experiment-deferral", "--scored-experiment-deferral-out", str(paths["scored"]), "--out-dir", str(out), "--allow-warnings"],
        ["build-archive-source-lock-deferral", "--archive-source-lock-deferral-out", str(paths["archive"]), "--out-dir", str(out), "--allow-warnings"],
        ["build-doc-staleness-validation", "--doc-staleness-validation-out", str(paths["docs"]), "--out-dir", str(out), "--allow-warnings"],
        ["build-next-stage-decision", "--next-stage-decision-out", str(paths["decision"]), "--out-dir", str(out), "--allow-warnings"],
    ]
    for command in commands:
        result = runner.invoke(app, command)
        assert result.exit_code == 0, result.output

    summary_args = [
        "build-summary",
        "--formula-parity-report", str(paths["formula"]),
        "--reference-contract-repair", str(paths["contract"]),
        "--hash-material-policy", str(paths["policy"]),
        "--result-store-integration", str(paths["result"]),
        "--score-summary-integration", str(paths["score"]),
        "--method-status-impact", str(paths["method"]),
        "--generated-body-policy", str(paths["body"]),
        "--full-p56-blocker", str(paths["full"]),
        "--scored-experiment-deferral", str(paths["scored"]),
        "--archive-source-lock-deferral", str(paths["archive"]),
        "--doc-staleness-validation", str(paths["docs"]),
        "--next-stage-decision", str(paths["decision"]),
        "--summary-out", str(paths["summary"]),
        "--out-dir", str(out),
        "--allow-warnings",
    ]
    assert runner.invoke(app, summary_args).exit_code == 0

    validate_args = [
        "validate-stage5ae",
        "--formula-parity-report", str(paths["formula"]),
        "--reference-contract-repair", str(paths["contract"]),
        "--hash-material-policy", str(paths["policy"]),
        "--result-store-integration", str(paths["result"]),
        "--score-summary-integration", str(paths["score"]),
        "--method-status-impact", str(paths["method"]),
        "--generated-body-policy", str(paths["body"]),
        "--full-p56-blocker", str(paths["full"]),
        "--scored-experiment-deferral", str(paths["scored"]),
        "--archive-source-lock-deferral", str(paths["archive"]),
        "--doc-staleness-validation", str(paths["docs"]),
        "--next-stage-decision", str(paths["decision"]),
        "--summary", str(paths["summary"]),
        "--results-dir", str(out),
    ]
    assert runner.invoke(app, validate_args).exit_code == 0
    assert runner.invoke(app, ["summary", "--summary", str(paths["summary"])]).exit_code == 0
