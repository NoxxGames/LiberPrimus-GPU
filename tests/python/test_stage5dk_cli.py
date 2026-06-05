from __future__ import annotations

import subprocess
import sys

from test_stage5dk_common import ROOT, ensure_stage5dk_built


def run_cli(*args: str) -> str:
    result = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "token-block", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_stage5dk_cli_validate_and_summary() -> None:
    ensure_stage5dk_built()

    validate_output = run_cli("validate-stage5dk")
    assert "token_block_stage5dk_valid=true" in validate_output

    summary_output = run_cli("stage5dk-summary")
    assert "stage_id=stage-5dk" in summary_output
    assert "fandom_source_count=14" in summary_output
    assert "page56_hash_bits=512" in summary_output
    assert "page56_algorithm_known=false" in summary_output
    assert "pivot_target_selected=false" in summary_output
    assert "recommended_next_stage_id=stage-5dl" in summary_output


def test_stage5dk_focused_cli_commands() -> None:
    ensure_stage5dk_built()

    focused_commands = [
        (
            "validate-stage5dk-fandom-source-locks",
            "token_block_stage5dk_fandom_source_locks_valid=true",
        ),
        (
            "validate-stage5dk-existing-source-crosswalk",
            "token_block_stage5dk_existing_source_crosswalk_valid=true",
        ),
        (
            "validate-stage5dk-page56-hash-contract",
            "token_block_stage5dk_page56_hash_contract_valid=true",
        ),
        ("validate-stage5dk-pivot-readiness", "token_block_stage5dk_pivot_readiness_valid=true"),
        (
            "validate-stage5dk-stage5dj-preservation",
            "token_block_stage5dk_stage5dj_preservation_valid=true",
        ),
        (
            "validate-stage5dk-stage5dg-preservation",
            "token_block_stage5dk_stage5dg_preservation_valid=true",
        ),
        (
            "validate-stage5dk-stage5bd-preservation",
            "token_block_stage5dk_stage5bd_preservation_valid=true",
        ),
        (
            "validate-stage5dk-active-lineage-preservation",
            "token_block_stage5dk_active_lineage_preservation_valid=true",
        ),
        ("validate-stage5dk-sidecar-gates", "token_block_stage5dk_sidecar_gates_valid=true"),
        (
            "validate-stage5dk-handoff-continuity",
            "token_block_stage5dk_handoff_continuity_valid=true",
        ),
        (
            "validate-stage5dk-credential-redaction-policy",
            "token_block_stage5dk_credential_redaction_policy_valid=true",
        ),
        (
            "validate-stage5dk-governance-scope",
            "token_block_stage5dk_governance_scope_valid=true",
        ),
    ]
    for command, expected in focused_commands:
        assert expected in run_cli(command)


def test_stage5dk_build_cli_is_registered() -> None:
    output = run_cli("build-stage5dk", "--help")

    assert "build-stage5dk" in output
