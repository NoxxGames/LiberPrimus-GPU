import subprocess
import sys

from test_stage5cy_common import ROOT


def _run(*args: str) -> str:
    result = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "token-block", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_stage5cy_cli_build_validate_and_summary() -> None:
    assert "stage_id=stage-5cy" in _run("build-stage5cy")
    assert "token_block_stage5cy_stage5cx_findings_valid=true" in _run(
        "validate-stage5cy-stage5cx-findings"
    )
    assert "token_block_stage5cy_operator_option_selection_preflight_valid=true" in _run(
        "validate-stage5cy-operator-option-selection-preflight"
    )
    assert "token_block_stage5cy_validation_count_reconciliation_valid=true" in _run(
        "validate-stage5cy-validation-count-reconciliation"
    )
    assert "token_block_stage5cy_valid=true" in _run("validate-stage5cy")
    assert "recommended_next_stage_id=stage-5cz" in _run("stage5cy-summary")


def test_stage5cw_cli_command_still_works() -> None:
    assert "token_block_stage5cw_valid=true" in _run("validate-stage5cw")
