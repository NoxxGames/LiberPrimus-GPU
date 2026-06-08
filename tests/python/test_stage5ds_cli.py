from __future__ import annotations

from test_stage5ds_common import ensure_stage5ds_built, run_token_block_cli


def test_stage5ds_cli_validate_and_summary() -> None:
    ensure_stage5ds_built()
    validate_output = run_token_block_cli("validate-stage5ds")
    assert "token_block_stage5ds_valid=true" in validate_output

    summary_output = run_token_block_cli("stage5ds-summary")
    assert "music_candidate_records_created=11" in summary_output
    assert "recommended_next_stage_id=stage-5dt" in summary_output


def test_stage5ds_focused_validators_registered() -> None:
    ensure_stage5ds_built()
    commands = [
        ("validate-stage5ds-music-source-lock", "token_block_stage5ds_music_source_lock_valid=true"),
        ("validate-stage5ds-music-file-inventory", "token_block_stage5ds_music_file_inventory_valid=true"),
        ("validate-stage5ds-music-message-anchors", "token_block_stage5ds_music_message_anchors_valid=true"),
        ("validate-stage5ds-music-candidates", "token_block_stage5ds_music_candidates_valid=true"),
        ("validate-stage5ds-ouroboros-context", "token_block_stage5ds_ouroboros_context_valid=true"),
        (
            "validate-stage5ds-token-block-static-context",
            "token_block_stage5ds_token_block_static_context_valid=true",
        ),
        ("validate-stage5ds-chatgpt-context", "token_block_stage5ds_chatgpt_context_valid=true"),
        (
            "validate-stage5ds-source-browser-loadability",
            "token_block_stage5ds_source_browser_loadability_valid=true",
        ),
        ("validate-stage5ds-scope-control", "token_block_stage5ds_scope_control_valid=true"),
    ]
    for command, marker in commands:
        assert marker in run_token_block_cli(command)
