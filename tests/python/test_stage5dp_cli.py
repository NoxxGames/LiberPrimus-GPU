from __future__ import annotations

import subprocess
import sys

from test_stage5dp_common import ROOT, ensure_stage5dp_built


def run_cli(*args: str) -> str:
    result = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "token-block", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_stage5dp_cli_validate_and_summary() -> None:
    ensure_stage5dp_built()

    validate_output = run_cli("validate-stage5dp")
    assert "token_block_stage5dp_valid=true" in validate_output

    summary_output = run_cli("stage5dp-summary")
    assert "stage_id=stage-5dp" in summary_output
    assert "new_reddit_source_lock_created=true" in summary_output
    assert "mayfly_docx_source_locked=true" in summary_output
    assert "mayfly_xlsx_source_locked=true" in summary_output
    assert "candidate_records_created=23" in summary_output
    assert "route_extraction_performed=false" in summary_output
    assert "recommended_next_stage_id=stage-5dq" in summary_output


def test_stage5dp_focused_cli_commands() -> None:
    ensure_stage5dp_built()

    focused_commands = [
        ("validate-stage5dp-new-reddit-source-lock", "token_block_stage5dp_new_reddit_source_lock_valid=true"),
        ("validate-stage5dp-mayfly-source-lock", "token_block_stage5dp_mayfly_source_lock_valid=true"),
        ("validate-stage5dp-mayfly-workbook-summary", "token_block_stage5dp_mayfly_workbook_summary_valid=true"),
        ("validate-stage5dp-dot-observations", "token_block_stage5dp_dot_observations_valid=true"),
        ("validate-stage5dp-front-cover-measurements", "token_block_stage5dp_front_cover_measurements_valid=true"),
        ("validate-stage5dp-iso-and-problems-sources", "token_block_stage5dp_iso_and_problems_sources_valid=true"),
        ("validate-stage5dp-chatgpt-context-file", "token_block_stage5dp_chatgpt_context_file_valid=true"),
        ("validate-stage5dp-sidecar-gates", "token_block_stage5dp_sidecar_gates_valid=true"),
        ("validate-stage5dp-handoff-continuity", "token_block_stage5dp_handoff_continuity_valid=true"),
    ]
    for command, expected in focused_commands:
        assert expected in run_cli(command)


def test_stage5dp_build_cli_is_registered() -> None:
    output = run_cli("build-stage5dp", "--help")

    assert "build-stage5dp" in output
