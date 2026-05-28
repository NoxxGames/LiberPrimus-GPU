from test_stage5bk_common import load_yaml


def test_stage5bk_iddqd_v2_byte_strings_are_metadata_only() -> None:
    payload = load_yaml("data/historical-route/stage5bk-iddqd-v2-byte-strings-source-lock.yaml")
    assert payload["byte_strings_source_found"] is True
    assert payload["byte_string_count"] == 4
    assert payload["exact_512_hex_string_count"] == 4
    assert payload["source_string_bodies_committed"] is False
    assert payload["decoded_byte_bodies_committed"] is False
    assert payload["string1_to_3_stage5bj_crosswalk_count"] == 3
    assert all(record["hex_length"] == 512 for record in payload["records"])
    assert all(record["decoded_byte_hash_role"] == "provenance_only_not_search" for record in payload["records"])
