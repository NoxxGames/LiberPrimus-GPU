from __future__ import annotations

import subprocess
import sys

from test_stage5dq_common import ROOT, ensure_stage5dq_built


def run_token_block_cli(*args: str) -> str:
    result = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "token-block", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_stage5dq_cli_validate_and_summary() -> None:
    ensure_stage5dq_built()

    validate_output = run_token_block_cli("validate-stage5dq")
    assert "token_block_stage5dq_valid=true" in validate_output

    summary_output = run_token_block_cli("stage5dq-summary")
    assert "stage_id=stage-5dq" in summary_output
    assert "source_browser_gui_implemented_now=true" in summary_output
    assert "route_extraction_performed_now=false" in summary_output
    assert "recommended_next_stage_id=stage-5dr" in summary_output


def test_stage5dq_build_cli_is_registered() -> None:
    output = run_token_block_cli("build-stage5dq", "--help")

    assert "build-stage5dq" in output
