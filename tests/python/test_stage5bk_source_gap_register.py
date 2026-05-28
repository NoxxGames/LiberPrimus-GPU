from test_stage5bk_common import load_yaml


def test_stage5bk_iddqd_v2_source_gap_register_is_metadata_only() -> None:
    payload = load_yaml("data/historical-route/stage5bk-iddqd-v2-source-gap-register.yaml")
    assert payload["source_gap_count"] == len(payload["records"])
    assert payload["execution_allowed"] is False
    assert payload["solve_claim"] is False
