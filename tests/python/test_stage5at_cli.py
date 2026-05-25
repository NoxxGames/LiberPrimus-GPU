import subprocess
import sys


def test_stage5at_validate_cli_passes() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "token-block", "validate-stage5at"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "token_block_stage5at_valid=true" in result.stdout
    assert "case_review_challenge_count=203" in result.stdout
