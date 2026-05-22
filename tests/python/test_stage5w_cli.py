from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5w_cli_build_and_validate(tmp_path: Path) -> None:
    runner = CliRunner()
    source = tmp_path / "source.yaml"
    contract = tmp_path / "contract.yaml"
    schedule = tmp_path / "schedule.yaml"
    mapping = tmp_path / "mapping.yaml"
    prep = tmp_path / "prep.yaml"
    result = tmp_path / "result.yaml"
    guardrail = tmp_path / "guardrail.yaml"
    decision = tmp_path / "decision.yaml"
    summary = tmp_path / "summary.yaml"
    commands = [
        ["prime-minus-one-native-contract", "build-source-inventory", "--source-inventory-out", str(source), "--out-dir", str(tmp_path), "--allow-warnings"],
        ["prime-minus-one-native-contract", "build-stream-contract", "--stream-contract-out", str(contract), "--out-dir", str(tmp_path), "--allow-warnings"],
        ["prime-minus-one-native-contract", "build-prime-schedule", "--prime-schedule-out", str(schedule), "--out-dir", str(tmp_path), "--allow-warnings"],
        ["prime-minus-one-native-contract", "build-candidate-batch-mapping", "--candidate-batch-mapping-out", str(mapping), "--out-dir", str(tmp_path), "--allow-warnings"],
        ["prime-minus-one-native-contract", "build-native-parity-preparation", "--native-parity-preparation-out", str(prep), "--out-dir", str(tmp_path), "--allow-warnings"],
        ["prime-minus-one-native-contract", "build-result-store-preflight", "--result-store-preflight-out", str(result), "--out-dir", str(tmp_path), "--allow-warnings"],
        ["prime-minus-one-native-contract", "build-guardrails", "--guardrail-out", str(guardrail), "--out-dir", str(tmp_path), "--allow-warnings"],
        ["prime-minus-one-native-contract", "build-next-stage-decision", "--next-stage-decision-out", str(decision), "--out-dir", str(tmp_path), "--allow-warnings"],
        [
            "prime-minus-one-native-contract",
            "build-summary",
            "--source-inventory",
            str(source),
            "--stream-contract",
            str(contract),
            "--prime-schedule",
            str(schedule),
            "--candidate-batch-mapping",
            str(mapping),
            "--native-parity-preparation",
            str(prep),
            "--result-store-preflight",
            str(result),
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
            "prime-minus-one-native-contract",
            "validate-stage5w",
            "--source-inventory",
            str(source),
            "--stream-contract",
            str(contract),
            "--prime-schedule",
            str(schedule),
            "--candidate-batch-mapping",
            str(mapping),
            "--native-parity-preparation",
            str(prep),
            "--result-store-preflight",
            str(result),
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
    assert "prime_minus_one_native_contract_stage5w_valid=true" in validation.output


def test_stage5w_summary_cli() -> None:
    result = CliRunner().invoke(
        app,
        ["prime-minus-one-native-contract", "summary", "--summary", "data/cuda/stage5w-prime-minus-one-native-contract-summary.yaml"],
    )
    assert result.exit_code == 0, result.output
    assert "recommended_next_stage_title=Stage 5X" in result.output

