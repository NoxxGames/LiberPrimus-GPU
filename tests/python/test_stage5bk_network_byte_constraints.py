from test_stage5bk_common import load_yaml


def test_stage5bk_network_byte_constraints_do_not_run_hash_search() -> None:
    payload = load_yaml("data/historical-route/stage5bk-network-byte-channel-constraint-integration.yaml")
    assert payload["byte_string_count"] == 4
    assert payload["exact_512_hex_string_count"] == 4
    assert payload["dwh_hash_search_performed"] is False
    assert payload["hash_search_performed"] is False
    assert payload["real_byte_stream_generated"] is False
