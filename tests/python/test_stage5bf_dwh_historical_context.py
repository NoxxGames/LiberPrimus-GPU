from test_stage5bf_local_archive_location import load_yaml


def test_stage5bf_dwh_context_is_not_operational_or_searched() -> None:
    payload = load_yaml("data/historical-route/stage5bf-dwh-historical-context.yaml")

    assert payload["dwh_defined"] is True
    assert payload["dwh_operational_status"] == "not_operational"
    assert payload["hash_search_performed"] is False
    assert payload["hash_comparison_performed"] is False
    assert payload["hash_preimage_claim"] is False
    assert payload["decode_claim"] is False
