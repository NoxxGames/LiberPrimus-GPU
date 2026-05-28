from test_stage5bn_common import load_yaml


def test_stage5bn_token_block_lineage_is_preserved() -> None:
    payload = load_yaml("data/token-block/stage5bn-token-block-lineage-preservation.yaml")

    assert payload["canonical_transcription_changed"] is False
    assert payload["stage5aw_branch_manifest_changed"] is False
    assert payload["stage5az_variant_family_manifest_changed"] is False
    assert payload["active_token_block_manifest_changed"] is False
    assert payload["stage5bd_dry_run_records_remain_valid"] is True
    assert payload["future_token_block_execution_remains_blocked"] is True
    assert payload["real_token_block_byte_streams_generated"] is False
    assert payload["variant_byte_streams_generated"] is False
