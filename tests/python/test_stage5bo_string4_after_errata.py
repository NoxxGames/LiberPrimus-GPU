from test_stage5bo_common import load_yaml


def test_stage5bo_string4_becomes_full_planning_branch_match() -> None:
    payload = load_yaml("data/token-block/stage5bo-string4-branch-membership-after-errata.yaml")

    assert payload["string4_position_count_checked"] == 256
    assert payload["string4_branch_membership_status_before_errata"] == "partial_branch_match"
    assert payload["string4_branch_membership_status_after_errata"] == "full_branch_match"
    assert payload["canonical_match_count"] == 249
    assert payload["stage5aw_supported_noncanonical_count"] == 6
    assert payload["operator_errata_supported_noncanonical_count"] == 1
    assert payload["unsupported_position_count"] == 0
    assert payload["target_199_after"]["operator_errata_supported"] is True
    assert payload["real_byte_stream_generated"] is False
