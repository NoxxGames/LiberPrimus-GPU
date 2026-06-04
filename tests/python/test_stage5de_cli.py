from __future__ import annotations

import subprocess
import sys

from test_stage5de_common import ROOT, SELECTED_OPTION_ID


def _run(*args: str) -> str:
    result = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "token-block", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_stage5de_cli_build_validate_and_summary() -> None:
    assert "stage_id=stage-5de" in _run("build-stage5de")
    assert "token_block_stage5de_stage5dd_findings_valid=true" in _run(
        "validate-stage5de-stage5dd-findings"
    )
    assert "token_block_stage5de_review_label_anomaly_valid=true" in _run(
        "validate-stage5de-review-label-anomaly"
    )
    assert "token_block_stage5de_real_operator_approval_preparation_valid=true" in _run(
        "validate-stage5de-real-operator-approval-preparation"
    )
    assert "token_block_stage5de_valid=true" in _run("validate-stage5de")
    summary = _run("stage5de-summary")
    assert f"selected_option_id={SELECTED_OPTION_ID}" in summary
    assert "recommended_next_stage_id=stage-5df" in summary


def test_stage5dc_cli_command_still_works_after_stage5de() -> None:
    assert "token_block_stage5dc_valid=true" in _run("validate-stage5dc")
