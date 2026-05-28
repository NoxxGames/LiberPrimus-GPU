from test_stage5bm_common import load_yaml


def test_stage5bm_dwh_quarantine_reaffirmed() -> None:
    record = load_yaml("data/historical-route/stage5bm-dwh-quarantine-reaffirmation.yaml")

    assert record["dwh_expansion"] == "Deep Web Hash"
    assert record["dwh_operational_status"] == "not_operational"
    assert record["string4_dwh_status"] == "not_a_dwh_target"
    assert record["hash_search_performed"] is False
    assert record["decode_attempt_performed"] is False
