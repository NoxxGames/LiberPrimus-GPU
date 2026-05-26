from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_stage5aw_cli_validate_stage5aw_works_from_committed_records() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "token-block", "validate-stage5aw"],
        check=False,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "token_block_stage5aw_valid=true" in result.stdout
    assert "stage5av_malformed_extras_found=3" in result.stdout
