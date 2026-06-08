from __future__ import annotations

import subprocess
import sys

from test_stage5dr_common import ROOT, ensure_stage5dr_built


def run_token_block_cli(*args: str) -> str:
    result = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "token-block", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_stage5dr_cli_validate_and_summary() -> None:
    ensure_stage5dr_built()

    validate_output = run_token_block_cli("validate-stage5dr")
    assert "token_block_stage5dr_valid=true" in validate_output

    summary_output = run_token_block_cli("stage5dr-summary")
    assert "stage_id=stage-5dr" in summary_output
    assert "bottom_details_panel_spans_categories_and_table=true" in summary_output
    assert "status_unspecified_display_added=true" in summary_output
    assert "execution_performed=false" in summary_output
    assert "recommended_next_stage_id=stage-5ds" in summary_output


def test_stage5dr_focused_validators_registered() -> None:
    ensure_stage5dr_built()
    commands = [
        ("validate-stage5dr-detail-panel", "token_block_stage5dr_detail_panel_valid=true"),
        ("validate-stage5dr-table-context-menu", "token_block_stage5dr_table_context_menu_valid=true"),
        ("validate-stage5dr-status-display", "token_block_stage5dr_status_display_valid=true"),
        (
            "validate-stage5dr-image-thumbnail-actions",
            "token_block_stage5dr_image_thumbnail_actions_valid=true",
        ),
        ("validate-stage5dr-url-file-actions", "token_block_stage5dr_url_file_actions_valid=true"),
        ("validate-stage5dr-preservation", "token_block_stage5dr_preservation_valid=true"),
    ]
    for command, expected in commands:
        assert expected in run_token_block_cli(command)
