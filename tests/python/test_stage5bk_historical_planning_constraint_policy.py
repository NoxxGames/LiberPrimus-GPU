from test_stage5bk_common import load_yaml


def test_stage5bk_constraint_policy_blocks_execution() -> None:
    payload = load_yaml("data/historical-route/stage5bk-historical-planning-constraint-policy.yaml")
    assert payload["constraint_count"] == len(payload["constraints"])
    assert "iddqd_v2_byte_strings_are_source_lock_metadata_not_dwh_targets" in payload["constraints"]
    assert payload["future_token_block_execution_remains_blocked"] is True
    assert payload["execution_allowed"] is False
