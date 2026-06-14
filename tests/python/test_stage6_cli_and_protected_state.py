from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from libreprimus.token_block import stage6
from test_stage6_common import stage6_data


def test_stage6_cli_validate_and_summary_work() -> None:
    validate = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "token-block", "validate-stage6"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert validate.returncode == 0
    assert "token_block_stage6_valid=true" in validate.stdout

    summary = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "token-block", "stage6-summary"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert summary.returncode == 0
    assert "recommended_next_stage_id=stage-6b" in summary.stdout


def test_stage6_protected_local_state_recorded_but_not_stage6_outputs() -> None:
    payload = stage6_data("reviewable_validation_evidence")
    assert payload["protected_local_paths"] == stage6.PROTECTED_LOCAL_PATHS
    assert payload["protected_local_paths_staged"] is False
    output_paths = {path.as_posix() for path in stage6.DATA_PATHS.values()}
    assert not output_paths.intersection(stage6.PROTECTED_LOCAL_PATHS)


def test_stage6_codex_output_handoff_path_is_ignored() -> None:
    handoff = stage6_data("codex_handoff_policy")
    assert handoff["completion_summary_path"] == "codex-output/stage6-codex-completion.md"
    result = subprocess.run(
        ["git", "check-ignore", "-q", "codex-output/stage6-codex-completion.md"],
        check=False,
    )
    assert result.returncode == 0
    assert not Path("codex_output").exists()
