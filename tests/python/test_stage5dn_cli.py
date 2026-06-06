from __future__ import annotations

import subprocess
import sys

from test_stage5dn_common import ROOT, ensure_stage5dn_built


def run_cli(*args: str) -> str:
    result = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "token-block", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_stage5dn_cli_validate_and_summary() -> None:
    ensure_stage5dn_built()

    validate_output = run_cli("validate-stage5dn")
    assert "token_block_stage5dn_valid=true" in validate_output

    summary_output = run_cli("stage5dn-summary")
    assert "stage_id=stage-5dn" in summary_output
    assert "disk_cipher_v1_source_lock_created=true" in summary_output
    assert "disk_results_png_source_locked=true" in summary_output
    assert "target_selected=false" in summary_output
    assert "execution_authorized_now=false" in summary_output
    assert "recommended_next_stage_id=stage-5do" in summary_output


def test_stage5dn_focused_cli_commands() -> None:
    ensure_stage5dn_built()

    focused_commands = [
        ("validate-stage5dn-disk-source-lock", "token_block_stage5dn_disk_source_lock_valid=true"),
        ("validate-stage5dn-results-png", "token_block_stage5dn_results_png_valid=true"),
        ("validate-stage5dn-message-bodies", "token_block_stage5dn_message_bodies_valid=true"),
        (
            "validate-stage5dn-disk-56311-wynn-way",
            "token_block_stage5dn_disk_56311_wynn_way_valid=true",
        ),
        (
            "validate-stage5dn-disk-p39-row1-cluster",
            "token_block_stage5dn_disk_p39_row1_cluster_valid=true",
        ),
        ("validate-stage5dn-doublet-suppression", "token_block_stage5dn_doublet_suppression_valid=true"),
        (
            "validate-stage5dn-probability-quarantine",
            "token_block_stage5dn_probability_quarantine_valid=true",
        ),
        (
            "validate-stage5dn-circumference-precedent",
            "token_block_stage5dn_circumference_precedent_valid=true",
        ),
        (
            "validate-stage5dn-pdd-triangle-56311-update",
            "token_block_stage5dn_pdd_triangle_56311_update_valid=true",
        ),
        (
            "validate-stage5dn-stage5dm-preservation",
            "token_block_stage5dn_stage5dm_preservation_valid=true",
        ),
        (
            "validate-stage5dn-stage5bd-preservation",
            "token_block_stage5dn_stage5bd_preservation_valid=true",
        ),
        (
            "validate-stage5dn-active-lineage-preservation",
            "token_block_stage5dn_active_lineage_preservation_valid=true",
        ),
        ("validate-stage5dn-sidecar-gates", "token_block_stage5dn_sidecar_gates_valid=true"),
        (
            "validate-stage5dn-handoff-continuity",
            "token_block_stage5dn_handoff_continuity_valid=true",
        ),
        ("validate-stage5dn-governance-scope", "token_block_stage5dn_governance_scope_valid=true"),
    ]
    for command, expected in focused_commands:
        assert expected in run_cli(command)


def test_stage5dn_build_cli_is_registered() -> None:
    output = run_cli("build-stage5dn", "--help")

    assert "build-stage5dn" in output
