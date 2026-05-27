from test_stage5bf_local_archive_location import load_yaml


def test_stage5bf_source_gap_register_routes_gaps_to_deep_research() -> None:
    payload = load_yaml("data/historical-route/stage5bf-source-gap-register.yaml")
    gap_ids = {gap["gap_id"] for gap in payload["gaps"]}

    assert payload["source_gap_count"] == 4
    assert "pgp_online_verification_not_performed" in gap_ids
    assert "dwh_relationship_remains_speculative" in gap_ids
    assert {gap["status"] for gap in payload["gaps"]} == {"requires_deep_research_review"}
