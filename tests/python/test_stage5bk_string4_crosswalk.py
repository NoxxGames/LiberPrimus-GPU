from test_stage5bk_common import load_yaml


def test_stage5bk_string4_crosswalk_records_hash_comparison_as_metadata() -> None:
    payload = load_yaml("data/token-block/stage5bk-page49-51-string4-crosswalk.yaml")
    assert len(payload["source_string4_hex_sha256"]) == 64
    assert len(payload["source_string4_decoded_byte_sha256"]) == 64
    assert payload["hash_search_performed"] is False
    assert payload["decode_attempt_performed"] is False
