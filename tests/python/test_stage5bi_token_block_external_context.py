from test_stage5bi_fandom_page_triage import load_yaml


def test_stage5bi_token_block_external_context_preserves_active_lineage() -> None:
    payload = load_yaml("data/token-block/stage5bi-token-block-external-context.yaml")
    urls = {record["source_url"] for record in payload["context_records"]}

    assert "https://uncovering-cicada.fandom.com/wiki/Page_49-51" in urls
    assert payload["canonical_transcription_changed"] is False
    assert payload["active_token_block_manifest_changed"] is False
    assert payload["stage5bd_dry_run_records_remain_valid"] is True
    assert payload["future_token_block_execution_remains_blocked"] is True
    assert payload["variant_byte_streams_generated"] is False
    assert payload["execution_allowed"] is False


def test_stage5bi_2014_surface_token_block_context_blocks_combination() -> None:
    payload = load_yaml("data/token-block/stage5bi-2014-surface-token-block-context.yaml")

    assert payload["surface_ids"] == [
        "stage5bi-c01-2014-growing-hex-surface",
        "stage5bi-c02-2014-1033-hex-surface",
        "stage5bi-c03-2014-3301-hex-surface",
    ]
    assert payload["page49_51_surface_id"] == "stage5bi-c04-page49-51-256-token-surface"
    assert payload["context_only"] is True
    assert payload["combination_allowed"] is False
    assert payload["hash_search_performed"] is False
    assert payload["decode_attempt_performed"] is False
