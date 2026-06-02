import subprocess

from test_stage5cw_common import ROOT


def _run(*args: str) -> str:
    result = subprocess.run(
        [".venv/Scripts/python.exe", "-m", "libreprimus.cli", "token-block", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_stage5cw_cli_build_validate_and_summary() -> None:
    assert "stage_id=stage-5cw" in _run("build-stage5cw")
    assert "token_block_stage5cw_stage5cv_findings_valid=true" in _run(
        "validate-stage5cw-stage5cv-findings"
    )
    assert "token_block_stage5cw_real_decision_package_preflight_valid=true" in _run(
        "validate-stage5cw-real-decision-package-preflight"
    )
    assert "token_block_stage5cw_valid=true" in _run("validate-stage5cw")
    assert "recommended_next_stage_id=stage-5cx" in _run("stage5cw-summary")
