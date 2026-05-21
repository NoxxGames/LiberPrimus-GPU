from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5q_cli_round_trip(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage5q"
    inventory = tmp_path / "inventory.yaml"
    mapping = tmp_path / "mapping.yaml"
    native = tmp_path / "native.yaml"
    preflight = tmp_path / "preflight.yaml"
    gate = tmp_path / "gate.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()
    commands = [
        [
            "gematria-expansion-candidate-mapping",
            "build-candidate-inventory",
            "--candidate-inventory-out",
            str(inventory),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-expansion-candidate-mapping",
            "build-token-mapping",
            "--candidate-inventory",
            str(inventory),
            "--token-mapping-out",
            str(mapping),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-expansion-candidate-mapping",
            "build-native-parity",
            "--token-mapping",
            str(mapping),
            "--native-parity-out",
            str(native),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-expansion-candidate-mapping",
            "build-result-store-preflight",
            "--token-mapping",
            str(mapping),
            "--native-parity",
            str(native),
            "--result-store-preflight-out",
            str(preflight),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-expansion-candidate-mapping",
            "build-expansion-gate",
            "--candidate-inventory",
            str(inventory),
            "--token-mapping",
            str(mapping),
            "--native-parity",
            str(native),
            "--result-store-preflight",
            str(preflight),
            "--expansion-gate-out",
            str(gate),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
        [
            "gematria-expansion-candidate-mapping",
            "build-summary",
            "--candidate-inventory",
            str(inventory),
            "--token-mapping",
            str(mapping),
            "--native-parity",
            str(native),
            "--result-store-preflight",
            str(preflight),
            "--expansion-gate",
            str(gate),
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
            "gematria-expansion-candidate-mapping",
            "validate-stage5q",
            "--candidate-inventory",
            str(inventory),
            "--token-mapping",
            str(mapping),
            "--native-parity",
            str(native),
            "--result-store-preflight",
            str(preflight),
            "--expansion-gate",
            str(gate),
            "--summary",
            str(summary),
            "--results-dir",
            str(out_dir),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "gematria_expansion_candidate_mapping_stage5q_valid=true" in validate.output
    assert "new_candidate_count=3" in validate.output

    printed = runner.invoke(
        app,
        ["gematria-expansion-candidate-mapping", "summary", "--summary", str(summary)],
    )
    assert printed.exit_code == 0, printed.output
    assert "cuda_execution_performed=False" in printed.output


def test_stage5q_cli_keeps_stage5p_command_registered() -> None:
    result = CliRunner().invoke(app, ["gematria-cuda-result-store", "summary", "--help"])
    assert result.exit_code == 0, result.output
