from test_stage5bn_common import load_yaml


def test_stage5bn_proposed_option_addendum_is_inactive_review_only() -> None:
    payload = load_yaml("data/token-block/stage5bn-proposed-token-option-addendum.yaml")

    assert payload["target_token_index_0_based"] == 199
    assert payload["stage5ap_canonical_token"] == "0I"
    assert payload["proposed_option"] == "0l"
    assert payload["proposed_option_addendum_status"] == "proposed_inactive_review_only"
    assert payload["active_stage5aw_records_mutated"] is False
    assert payload["active_stage5ay_records_mutated"] is False
    assert payload["active_stage5az_records_mutated"] is False
    assert payload["canonical_transcription_changed"] is False
    assert payload["active_token_block_manifest_changed"] is False
