from test_stage5bm_common import load_yaml


def test_stage5bm_primary60_inverse_policy_is_metadata_only() -> None:
    record = load_yaml("data/token-block/stage5bm-string4-primary60-inverse-policy.yaml")

    assert record["primary60_alphabet"] == "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwx"
    assert record["input_domain"] == "0_to_255_bytes"
    assert record["policy_scope"] == "string4_branch_membership_metadata_only"
    assert record["real_byte_stream_generated"] is False
    assert record["execution_allowed"] is False
