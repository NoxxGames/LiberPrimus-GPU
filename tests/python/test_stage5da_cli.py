from __future__ import annotations

import subprocess
import sys

from test_stage5da_common import ROOT


def _run(*args: str) -> str:
    result = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "token-block", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_stage5da_cli_build_validate_and_summary() -> None:
    assert "stage_id=stage-5da" in _run("build-stage5da")
    assert "token_block_stage5da_stage5cz_findings_valid=true" in _run(
        "validate-stage5da-stage5cz-findings"
    )
    assert "token_block_stage5da_choice_pause_scaffold_valid=true" in _run(
        "validate-stage5da-choice-pause-scaffold"
    )
    assert "token_block_stage5da_explicit_pause_nonactivation_valid=true" in _run(
        "validate-stage5da-explicit-pause-nonactivation"
    )
    assert "token_block_stage5da_valid=true" in _run("validate-stage5da")
    assert "recommended_next_stage_id=stage-5db" in _run("stage5da-summary")


def test_stage5cy_cli_command_still_works_after_stage5da() -> None:
    assert "token_block_stage5cy_validation_count_reconciliation_valid=true" in _run(
        "validate-stage5cy-validation-count-reconciliation"
    )
