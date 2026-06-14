from __future__ import annotations

from libreprimus.token_block import stage6
from test_stage6_common import stage6_data


def test_stage6_source_root_census_covers_required_roots() -> None:
    payload = stage6_data("third_party_source_root_census")
    root_ids = {root["root_id"] for root in payload["source_roots"]}
    assert root_ids == {root_id for root_id, *_ in stage6.SOURCE_ROOTS}
    assert payload["source_root_count"] == 25
    assert payload["full_recursive_third_party_hashing_performed"] is False


def test_stage6_large_roots_are_bounded_presence_only() -> None:
    payload = stage6_data("third_party_source_root_census")
    roots = {root["root_id"]: root for root in payload["source_roots"]}
    for root_id in stage6.LARGE_ROOT_IDS:
        assert roots[root_id]["bounded_inventory_mode"] == "presence_status_only"
        assert roots[root_id]["sha256_tree_digest_if_present"] is None


def test_stage6_observation_root_has_focused_digest_only() -> None:
    payload = stage6_data("third_party_source_root_census")
    obs = next(root for root in payload["source_roots"] if root["root_id"] == "observation_on_rune_frequency")
    assert obs["present_locally"] is True
    assert obs["bounded_inventory_mode"] == "focused_expected_file_inventory"
    assert obs["sha256_tree_digest_if_present"]
