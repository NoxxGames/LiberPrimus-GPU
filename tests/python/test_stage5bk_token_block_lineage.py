from test_stage5bk_common import load_yaml


def test_stage5bk_token_block_lineage_preserved() -> None:
    payload = load_yaml("data/token-block/stage5bk-token-block-lineage-preservation.yaml")
    assert payload["active_stage5aw_branch_manifest_preserved"] is True
    assert payload["active_stage5az_variant_family_manifest_preserved"] is True
    assert payload["stage5bd_active_manifest_lock_preserved"] is True
    assert payload["canonical_transcription_changed"] is False
    assert payload["active_token_block_manifest_changed"] is False
