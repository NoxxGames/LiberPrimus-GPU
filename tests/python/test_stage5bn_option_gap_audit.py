from test_stage5bn_common import load_yaml


def test_stage5bn_option_gap_preserves_stage5aw_gap() -> None:
    payload = load_yaml("data/token-block/stage5bn-stage5aw-option-gap-audit.yaml")

    assert payload["target_token_index_0_based"] == 199
    assert payload["stage5aw_allowed_tokens"] == ["0I", "0j", "OI", "Oj"]
    assert payload["stage5aw_supports_0l"] is False
    assert payload["stage5aw_supports_string4_target_option"] is False
    assert payload["option_gap_status"] == "unsupported"
    assert payload["active_records_mutated"] is False
    assert payload["proposed_addendum_required"] is True
