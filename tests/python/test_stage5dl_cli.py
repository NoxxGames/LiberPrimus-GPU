from __future__ import annotations

import subprocess
import sys

from test_stage5dl_common import ROOT, ensure_stage5dl_built


def run_cli(*args: str) -> str:
    result = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "token-block", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_stage5dl_cli_validate_and_summary() -> None:
    ensure_stage5dl_built()

    validate_output = run_cli("validate-stage5dl")
    assert "token_block_stage5dl_valid=true" in validate_output

    summary_output = run_cli("stage5dl-summary")
    assert "stage_id=stage-5dl" in summary_output
    assert "number_triangle_v1_source_locked=true" in summary_output
    assert "operator_preferred_future_target_family_id=pdd_153_triangle_word_prime_route_v1" in summary_output
    assert "pivot_target_selected_now=false" in summary_output
    assert "recommended_next_stage_id=stage-5dm" in summary_output


def test_stage5dl_focused_cli_commands() -> None:
    ensure_stage5dl_built()

    focused_commands = [
        ("validate-stage5dl-number-triangle-v1", "token_block_stage5dl_number_triangle_v1_valid=true"),
        ("validate-stage5dl-triangle-way-anchor", "token_block_stage5dl_triangle_way_anchor_valid=true"),
        ("validate-stage5dl-triangle-prime-mask", "token_block_stage5dl_triangle_prime_mask_valid=true"),
        (
            "validate-stage5dl-triangle-2016-prime-layer",
            "token_block_stage5dl_triangle_2016_prime_layer_valid=true",
        ),
        (
            "validate-stage5dl-triangle-fibonacci-prime-index",
            "token_block_stage5dl_triangle_fibonacci_prime_index_valid=true",
        ),
        (
            "validate-stage5dl-triangle-56311-wynn-way",
            "token_block_stage5dl_triangle_56311_wynn_way_valid=true",
        ),
        (
            "validate-stage5dl-disk-cipher-source-lock",
            "token_block_stage5dl_disk_cipher_source_lock_valid=true",
        ),
        (
            "validate-stage5dl-quote-dialogue-cribs",
            "token_block_stage5dl_quote_dialogue_cribs_valid=true",
        ),
        (
            "validate-stage5dl-koan-depiction-source-lock",
            "token_block_stage5dl_koan_depiction_source_lock_valid=true",
        ),
        (
            "validate-stage5dl-local-source-crosswalks",
            "token_block_stage5dl_local_source_crosswalks_valid=true",
        ),
        ("validate-stage5dl-pivot-readiness", "token_block_stage5dl_pivot_readiness_valid=true"),
        (
            "validate-stage5dl-stage5dg-preservation",
            "token_block_stage5dl_stage5dg_preservation_valid=true",
        ),
        (
            "validate-stage5dl-stage5bd-preservation",
            "token_block_stage5dl_stage5bd_preservation_valid=true",
        ),
        (
            "validate-stage5dl-active-lineage-preservation",
            "token_block_stage5dl_active_lineage_preservation_valid=true",
        ),
        ("validate-stage5dl-sidecar-gates", "token_block_stage5dl_sidecar_gates_valid=true"),
        (
            "validate-stage5dl-handoff-continuity",
            "token_block_stage5dl_handoff_continuity_valid=true",
        ),
        (
            "validate-stage5dl-credential-redaction-policy",
            "token_block_stage5dl_credential_redaction_policy_valid=true",
        ),
        ("validate-stage5dl-governance-scope", "token_block_stage5dl_governance_scope_valid=true"),
    ]
    for command, expected in focused_commands:
        assert expected in run_cli(command)


def test_stage5dl_build_cli_is_registered() -> None:
    output = run_cli("build-stage5dl", "--help")

    assert "build-stage5dl" in output
