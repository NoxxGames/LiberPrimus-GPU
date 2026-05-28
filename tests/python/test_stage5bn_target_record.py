from test_stage5bn_common import load_yaml


def test_stage5bn_target_record_is_exact_target_and_non_execution() -> None:
    payload = load_yaml("data/token-block/stage5bn-string4-unsupported-position-target.yaml")

    assert payload["target_token_index_0_based"] == 199
    assert payload["target_row_index_one_based"] == 25
    assert payload["target_column_index_one_based"] == 8
    assert payload["stage5ap_canonical_token"] == "0I"
    assert payload["string4_inferred_token"] == "0l"
    assert payload["stage5aw_allowed_tokens_summary"] == "0I, 0j, OI, Oj"
    assert payload["canonical_transcription_changed"] is False
    assert payload["active_token_block_manifest_changed"] is False
    assert payload["real_byte_stream_generated"] is False
    assert payload["execution_allowed"] is False
    assert payload["solve_claim"] is False
