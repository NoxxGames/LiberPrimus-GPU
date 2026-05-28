from test_stage5bk_common import load_yaml


def test_stage5bk_page49_string4_crosswalk_is_not_activation() -> None:
    payload = load_yaml("data/token-block/stage5bk-page49-51-string4-crosswalk.yaml")
    assert payload["source_string4_found"] is True
    assert payload["crosswalk_role"] == "metadata_only_provenance_crosswalk_not_active_input"
    assert payload["canonical_transcription_changed"] is False
    assert payload["active_token_block_manifest_changed"] is False
    assert payload["persisted_token_block_bytes_generated"] is False
    assert payload["real_byte_stream_generated"] is False
