from test_stage5bj_crosswalk_closure import load_yaml


def test_token_block_lineage_is_preserved() -> None:
    payload = load_yaml("data/token-block/stage5bj-token-block-lineage-preservation.yaml")

    assert payload["canonical_transcription_changed"] is False
    assert payload["active_token_block_manifest_changed"] is False
    assert payload["stage5bd_dry_run_records_remain_valid"] is True
    assert payload["future_token_block_execution_remains_blocked"] is True
    assert payload["real_token_block_byte_streams_generated"] is False
    assert payload["variant_byte_streams_generated"] is False
    assert payload["execution_allowed"] is False
    assert all(record["path_found"] for record in payload["records"])


def test_2014_surface_context_closure_blocks_page49_51_combination() -> None:
    payload = load_yaml("data/token-block/stage5bj-2014-surface-context-closure.yaml")

    assert payload["exact_512_hex_surface_locked_count"] == 3
    assert payload["page49_51_combination_allowed"] is False
    assert payload["fandom_surface_combination_performed"] is False
    assert payload["hash_search_performed"] is False
    assert payload["decode_attempt_performed"] is False
    assert payload["solve_claim"] is False
