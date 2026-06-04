from __future__ import annotations

import subprocess
import sys

from test_stage5dc_common import ROOT, SELECTED_OPTION_ID


def _run(*args: str) -> str:
    result = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "token-block", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_stage5dc_cli_build_validate_and_summary() -> None:
    assert "stage_id=stage-5dc" in _run("build-stage5dc")
    assert "token_block_stage5dc_stage5db_findings_valid=true" in _run(
        "validate-stage5dc-stage5db-findings"
    )
    assert "token_block_stage5dc_choice_decision_valid=true" in _run(
        "validate-stage5dc-choice-decision"
    )
    assert "token_block_stage5dc_selected_option_valid=true" in _run(
        "validate-stage5dc-selected-option"
    )
    assert "token_block_stage5dc_valid=true" in _run("validate-stage5dc")
    summary = _run("stage5dc-summary")
    assert f"selected_option_id={SELECTED_OPTION_ID}" in summary
    assert "recommended_next_stage_id=stage-5dd" in summary


def test_stage5da_cli_command_still_works_after_stage5dc() -> None:
    assert "token_block_stage5da_valid=true" in _run("validate-stage5da")
