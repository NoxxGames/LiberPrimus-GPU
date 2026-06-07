from __future__ import annotations

import subprocess
import sys

from test_stage5do_common import ROOT, ensure_stage5do_built


def run_cli(*args: str) -> str:
    result = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "token-block", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_stage5do_cli_validate_and_summary() -> None:
    ensure_stage5do_built()

    validate_output = run_cli("validate-stage5do")
    assert "token_block_stage5do_valid=true" in validate_output

    summary_output = run_cli("stage5do-summary")
    assert "stage_id=stage-5do" in summary_output
    assert "number_facts_collection_locked=true" in summary_output
    assert "potential_hint_locked=true" in summary_output
    assert "candidate_records_created=15" in summary_output
    assert "source_browser_gui_future_requirement_recorded=true" in summary_output
    assert "pivot_target_selected=false" in summary_output
    assert "execution_performed=false" in summary_output
    assert "recommended_next_stage_id=stage-5dp" in summary_output


def test_stage5do_focused_cli_commands() -> None:
    ensure_stage5do_built()

    focused_commands = [
        ("validate-stage5do-number-facts-source-lock", "token_block_stage5do_number_facts_source_lock_valid=true"),
        ("validate-stage5do-potential-hint-source-lock", "token_block_stage5do_potential_hint_source_lock_valid=true"),
        ("validate-stage5do-page32-red-header-2472", "token_block_stage5do_page32_red_header_2472_valid=true"),
        (
            "validate-stage5do-page32-red-header-463-3299",
            "token_block_stage5do_page32_red_header_463_3299_valid=true",
        ),
        ("validate-stage5do-no-f-section-flow", "token_block_stage5do_no_f_section_flow_valid=true"),
        ("validate-stage5do-doublet-v1", "token_block_stage5do_doublet_v1_valid=true"),
        ("validate-stage5do-pixel-colour-candidate", "token_block_stage5do_pixel_colour_candidate_valid=true"),
        ("validate-stage5do-gp-facts", "token_block_stage5do_gp_facts_valid=true"),
        (
            "validate-stage5do-source-browser-future-requirement",
            "token_block_stage5do_source_browser_future_requirement_valid=true",
        ),
        ("validate-stage5do-sidecar-gates", "token_block_stage5do_sidecar_gates_valid=true"),
        ("validate-stage5do-preservation", "token_block_stage5do_preservation_valid=true"),
        ("validate-stage5do-handoff-continuity", "token_block_stage5do_handoff_continuity_valid=true"),
    ]
    for command, expected in focused_commands:
        assert expected in run_cli(command)


def test_stage5do_build_cli_is_registered() -> None:
    output = run_cli("build-stage5do", "--help")

    assert "build-stage5do" in output
