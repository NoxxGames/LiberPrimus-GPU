from test_stage5bm_common import load_yaml


def test_stage5bm_summary_matches_branch_membership_record() -> None:
    summary = load_yaml("data/project-state/stage5bm-summary.yaml")
    branch = load_yaml("data/token-block/stage5bm-string4-stage5aw-branch-membership.yaml")

    assert summary["status"] == "complete"
    assert summary["string4_branch_membership_status"] == branch["string4_branch_membership_status"]
    assert summary["string4_canonical_match_count"] == branch["canonical_match_count"]
    assert summary["string4_stage5aw_supported_noncanonical_count"] == branch["stage5aw_supported_noncanonical_count"]
    assert summary["string4_unsupported_position_count"] == branch["unsupported_position_count"]
    assert summary["future_token_block_execution_remains_blocked"] is True
