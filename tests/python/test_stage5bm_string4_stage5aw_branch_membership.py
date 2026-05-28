from test_stage5bm_common import load_yaml


def test_stage5bm_string4_stage5aw_branch_membership_is_partial() -> None:
    record = load_yaml("data/token-block/stage5bm-string4-stage5aw-branch-membership.yaml")

    assert record["string4_branch_membership_status"] == "partial_branch_match"
    assert record["string4_position_count_checked"] == 256
    assert record["canonical_match_count"] == 249
    assert record["stage5aw_supported_noncanonical_count"] == 6
    assert record["unsupported_position_count"] == 1
    assert record["parser_inconclusive_position_count"] == 0
    assert record["unsupported_position_records"][0]["token_index_0_based"] == 199
    assert record["full_cartesian_product_enumerated"] is False
