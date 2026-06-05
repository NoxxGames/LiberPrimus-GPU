from __future__ import annotations

import subprocess
import sys

from test_stage5di_common import ROOT


def run_cli(*args: str) -> str:
    result = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "token-block", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_stage5di_cli_build_validate_and_summary() -> None:
    build_output = run_cli("build-stage5di")
    assert "pivot_target_selected_now=false" in build_output
    assert "recommended_next_stage_id=stage-5dj" in build_output

    validate_output = run_cli("validate-stage5di")
    assert "token_block_stage5di_valid=true" in validate_output

    summary_output = run_cli("stage5di-summary")
    assert "candidate_family_count=8" in summary_output
    assert "execution_authorized_now=false" in summary_output


def test_stage5di_focused_cli_commands() -> None:
    focused_commands = [
        (
            "validate-stage5di-source-lock-register",
            "token_block_stage5di_source_lock_register_valid=true",
        ),
        (
            "validate-stage5di-local-archive-crosswalk",
            "token_block_stage5di_local_archive_crosswalk_valid=true",
        ),
        (
            "validate-stage5di-number-triangle-crosswalk",
            "token_block_stage5di_number_triangle_crosswalk_valid=true",
        ),
        (
            "validate-stage5di-route-candidate-families",
            "token_block_stage5di_route_candidate_families_valid=true",
        ),
        (
            "validate-stage5di-pivot-readiness",
            "token_block_stage5di_pivot_readiness_valid=true",
        ),
        (
            "validate-stage5di-dinkus-visual-delimiter",
            "token_block_stage5di_dinkus_visual_delimiter_valid=true",
        ),
        (
            "validate-stage5di-stage5dg-preservation",
            "token_block_stage5di_stage5dg_preservation_valid=true",
        ),
        (
            "validate-stage5di-stage5bd-preservation",
            "token_block_stage5di_stage5bd_preservation_valid=true",
        ),
        (
            "validate-stage5di-active-lineage-preservation",
            "token_block_stage5di_active_lineage_preservation_valid=true",
        ),
        ("validate-stage5di-sidecar-gates", "token_block_stage5di_sidecar_gates_valid=true"),
        (
            "validate-stage5di-handoff-continuity",
            "token_block_stage5di_handoff_continuity_valid=true",
        ),
        (
            "validate-stage5di-credential-redaction-policy",
            "token_block_stage5di_credential_redaction_policy_valid=true",
        ),
        (
            "validate-stage5di-governance-scope",
            "token_block_stage5di_governance_scope_valid=true",
        ),
    ]
    for command, expected in focused_commands:
        assert expected in run_cli(command)
