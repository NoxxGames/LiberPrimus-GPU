from __future__ import annotations

import subprocess

from test_stage5dg_common import ROOT


def run_cli(*args: str) -> str:
    result = subprocess.run(
        [".venv/Scripts/python.exe", "-m", "libreprimus.cli", "token-block", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_stage5dg_cli_build_validate_and_summary() -> None:
    build_output = run_cli("build-stage5dg")
    assert "real_operator_approval_record_created_now=true" in build_output
    assert "combined_approval_gate_satisfied_now=false" in build_output
    assert "recommended_next_stage_id=stage-5dh" in build_output

    validate_output = run_cli("validate-stage5dg")
    assert "token_block_stage5dg_valid=true" in validate_output

    summary_output = run_cli("stage5dg-summary")
    assert "operator_approval_component_satisfied_now=true" in summary_output
    assert "execution_authorized_now=false" in summary_output


def test_stage5dg_focused_cli_commands_and_stage5de_preserved() -> None:
    focused_commands = [
        (
            "validate-stage5dg-real-operator-approval-record",
            "token_block_stage5dg_real_operator_approval_record_valid=true",
        ),
        (
            "validate-stage5dg-operator-approval-nonactivation",
            "token_block_stage5dg_operator_approval_nonactivation_valid=true",
        ),
        ("validate-stage5dg-combined-gate", "token_block_stage5dg_combined_gate_valid=true"),
        (
            "validate-stage5dg-activation-nonauthorization",
            "token_block_stage5dg_activation_nonauthorization_valid=true",
        ),
        ("validate-stage5dg-sidecar-gates", "token_block_stage5dg_sidecar_gates_valid=true"),
    ]
    for command, expected in focused_commands:
        assert expected in run_cli(command)

    assert "token_block_stage5de_valid=true" in run_cli("validate-stage5de")
