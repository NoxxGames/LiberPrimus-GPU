from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.bounded_p56_mismatch.cli import app

runner = CliRunner()


def test_stage5ad_fix_cli_builds_and_validates(tmp_path: Path) -> None:
    out = tmp_path / "out"
    paths = {
        "hash": tmp_path / "hash.yaml",
        "token": tmp_path / "token.yaml",
        "stream": tmp_path / "stream.yaml",
        "formula": tmp_path / "formula.yaml",
        "material": tmp_path / "material.yaml",
        "contract": tmp_path / "contract.yaml",
        "root": tmp_path / "root.yaml",
        "repair": tmp_path / "repair.yaml",
        "guard": tmp_path / "guard.yaml",
        "decision": tmp_path / "decision.yaml",
        "summary": tmp_path / "summary.yaml",
    }
    commands = [
        ["build-hash-lineage", "--hash-lineage-out", str(paths["hash"]), "--out-dir", str(out), "--allow-warnings"],
        ["build-token-trace", "--token-trace-out", str(paths["token"]), "--out-dir", str(out), "--allow-warnings"],
        ["build-stream-trace", "--stream-trace-out", str(paths["stream"]), "--out-dir", str(out), "--allow-warnings"],
        ["build-formula-trace", "--formula-trace-out", str(paths["formula"]), "--out-dir", str(out), "--allow-warnings"],
        ["build-hash-material-trace", "--hash-material-out", str(paths["material"]), "--out-dir", str(out), "--allow-warnings"],
        ["build-reference-contract", "--reference-contract-out", str(paths["contract"]), "--out-dir", str(out), "--allow-warnings"],
        ["build-root-cause", "--root-cause-out", str(paths["root"]), "--out-dir", str(out), "--allow-warnings"],
        ["build-repair-readiness", "--repair-readiness-out", str(paths["repair"]), "--out-dir", str(out), "--allow-warnings"],
        ["build-guardrails", "--guardrail-out", str(paths["guard"]), "--out-dir", str(out), "--allow-warnings"],
        ["build-next-stage-decision", "--next-stage-decision-out", str(paths["decision"]), "--out-dir", str(out), "--allow-warnings"],
        [
            "build-summary",
            "--hash-lineage",
            str(paths["hash"]),
            "--token-trace",
            str(paths["token"]),
            "--stream-trace",
            str(paths["stream"]),
            "--formula-trace",
            str(paths["formula"]),
            "--hash-material",
            str(paths["material"]),
            "--reference-contract",
            str(paths["contract"]),
            "--root-cause",
            str(paths["root"]),
            "--repair-readiness",
            str(paths["repair"]),
            "--guardrail",
            str(paths["guard"]),
            "--next-stage-decision",
            str(paths["decision"]),
            "--summary-out",
            str(paths["summary"]),
            "--out-dir",
            str(out),
            "--allow-warnings",
        ],
        [
            "validate-stage5ad-fix",
            "--hash-lineage",
            str(paths["hash"]),
            "--token-trace",
            str(paths["token"]),
            "--stream-trace",
            str(paths["stream"]),
            "--formula-trace",
            str(paths["formula"]),
            "--hash-material",
            str(paths["material"]),
            "--reference-contract",
            str(paths["contract"]),
            "--root-cause",
            str(paths["root"]),
            "--repair-readiness",
            str(paths["repair"]),
            "--guardrail",
            str(paths["guard"]),
            "--next-stage-decision",
            str(paths["decision"]),
            "--summary",
            str(paths["summary"]),
            "--results-dir",
            str(out),
        ],
    ]
    for command in commands:
        result = runner.invoke(app, command)
        assert result.exit_code == 0, result.output

    summary_result = runner.invoke(app, ["summary", "--summary", str(paths["summary"])])
    assert summary_result.exit_code == 0
    assert "expected_hash_reference_lineage_mismatch" in summary_result.output
