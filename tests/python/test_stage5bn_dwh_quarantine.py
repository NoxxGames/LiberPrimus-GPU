from test_stage5bn_common import load_yaml


def test_stage5bn_dwh_quarantine_remains_non_operational() -> None:
    payload = load_yaml("data/historical-route/stage5bn-dwh-quarantine-reaffirmation.yaml")

    assert payload["dwh_relationship_status"] == "speculative_source_lock_required"
    assert payload["dwh_operational_status"] == "not_operational"
    assert payload["string4_target_position_review_affects_dwh"] is False
    assert payload["dwh_hash_search_performed"] is False
    assert payload["hash_preimage_search_performed"] is False
    assert payload["decode_attempt_performed"] is False
