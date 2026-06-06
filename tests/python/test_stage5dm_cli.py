from __future__ import annotations

import subprocess
import sys

from test_stage5dm_common import ROOT, ensure_stage5dm_built


def run_cli(*args: str) -> str:
    result = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "token-block", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_stage5dm_cli_validate_and_summary() -> None:
    ensure_stage5dm_built()

    validate_output = run_cli("validate-stage5dm")
    assert "token_block_stage5dm_valid=true" in validate_output

    summary_output = run_cli("stage5dm-summary")
    assert "stage_id=stage-5dm" in summary_output
    assert "source_lock_addendum_created=true" in summary_output
    assert "page32_arithmetic_verified=true" in summary_output
    assert "target_selected=false" in summary_output
    assert "recommended_next_stage_id=stage-5dn" in summary_output


def test_stage5dm_focused_cli_commands() -> None:
    ensure_stage5dm_built()

    focused_commands = [
        ("validate-stage5dm-blake-source-family", "token_block_stage5dm_blake_source_family_valid=true"),
        (
            "validate-stage5dm-lp-sacred-book-overlays",
            "token_block_stage5dm_lp_sacred_book_overlays_valid=true",
        ),
        (
            "validate-stage5dm-magic-square-precedent",
            "token_block_stage5dm_magic_square_precedent_valid=true",
        ),
        (
            "validate-stage5dm-full-page-visual-motifs",
            "token_block_stage5dm_full_page_visual_motifs_valid=true",
        ),
        (
            "validate-stage5dm-page32-moebius-fibonacci",
            "token_block_stage5dm_page32_moebius_fibonacci_valid=true",
        ),
        (
            "validate-stage5dm-doublet-scarcity-feature",
            "token_block_stage5dm_doublet_scarcity_feature_valid=true",
        ),
        (
            "validate-stage5dm-evidence-atlas-readiness",
            "token_block_stage5dm_evidence_atlas_readiness_valid=true",
        ),
        ("validate-stage5dm-drive-path-hygiene", "token_block_stage5dm_drive_path_hygiene_valid=true"),
        ("validate-stage5dm-pivot-readiness", "token_block_stage5dm_pivot_readiness_valid=true"),
        ("validate-stage5dm-sidecar-gates", "token_block_stage5dm_sidecar_gates_valid=true"),
        (
            "validate-stage5dm-handoff-continuity",
            "token_block_stage5dm_handoff_continuity_valid=true",
        ),
        ("validate-stage5dm-governance-scope", "token_block_stage5dm_governance_scope_valid=true"),
    ]
    for command, expected in focused_commands:
        assert expected in run_cli(command)


def test_stage5dm_build_cli_is_registered() -> None:
    output = run_cli("build-stage5dm", "--help")

    assert "build-stage5dm" in output
