from test_stage5bo_common import load_yaml


def test_stage5bo_sidecar_integrates_case_199_without_mutating_active_records() -> None:
    payload = load_yaml("data/token-block/stage5bo-errata-aware-token-option-universe.yaml")
    target = payload["target_index_199"]

    assert payload["universe_status"] == "inactive_planning_sidecar"
    assert payload["active_stage5aw_records_mutated"] is False
    assert payload["active_stage5ay_records_mutated"] is False
    assert target["stage5aw_active_allowed_tokens_before_errata"] == ["0I", "0j", "OI", "Oj"]
    assert target["errata_aware_allowed_tokens_for_planning"] == ["0I", "0l", "OI", "Ol"]
    assert target["string4_option_0l_supported_by_errata"] is True
    assert payload["execution_allowed"] is False
