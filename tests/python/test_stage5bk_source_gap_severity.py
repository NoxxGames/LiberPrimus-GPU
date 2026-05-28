from test_stage5bk_common import load_yaml


def test_stage5bk_source_gap_severity_blocks_execution() -> None:
    payload = load_yaml("data/historical-route/stage5bk-source-gap-severity-register.yaml")
    assert payload["source_gap_severity_record_count"] == len(payload["records"]) == 7
    assert payload["blocking_source_gap_count"] == 7
    assert payload["severity_counts"]["high"] == 3
    assert all(record["blocks_execution"] is True for record in payload["records"])
