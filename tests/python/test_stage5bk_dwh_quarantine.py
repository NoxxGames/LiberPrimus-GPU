from test_stage5bk_common import load_yaml


def test_stage5bk_dwh_quarantine_reaffirmed() -> None:
    payload = load_yaml("data/historical-route/stage5bk-dwh-quarantine-reaffirmation.yaml")
    assert payload["dwh_quarantine_reaffirmed"] is True
    assert payload["hash_preimage_search_performed"] is False
    assert payload["execution_allowed"] is False
