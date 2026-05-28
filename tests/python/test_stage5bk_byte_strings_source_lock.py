from test_stage5bk_common import load_yaml


def test_stage5bk_decoded_hashes_are_not_search_execution() -> None:
    payload = load_yaml("data/historical-route/stage5bk-iddqd-v2-byte-strings-source-lock.yaml")
    assert all(record["decoded_byte_length"] == 256 for record in payload["records"])
    assert all(record["dwh_hash_search_performed"] is False for record in payload["records"])
    assert all(record["hash_search_performed"] is False for record in payload["records"])
