from test_stage5bo_common import load_yaml


def test_stage5bo_integrates_stage5bn_addendum_as_inactive_errata() -> None:
    payload = load_yaml("data/token-block/stage5bo-stage5bn-addendum-integration.yaml")

    assert payload["target_token_index_0_based"] == 199
    assert payload["stage5bn_proposed_option"] == "0l"
    assert payload["stage5bo_operator_errata_supports_option"] is True
    assert payload["addendum_integration_status"] == "integrated_as_inactive_operator_errata"
    assert payload["active_stage5aw_records_mutated"] is False
    assert payload["stage5bn_history_rewritten"] is False
