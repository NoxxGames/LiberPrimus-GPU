from test_stage5bm_common import load_yaml


def test_stage5bm_stage5bj_errata_supersession_is_planning_only() -> None:
    record = load_yaml("data/historical-route/stage5bm-stage5bj-errata-supersession.yaml")

    assert record["supersedes_for_planning"] is True
    assert record["stage5bj_historical_records_mutated"] is False
    assert record["route_equivalent_file_is_page_body_snapshot"] is False
    assert record["route_equivalent_file_is_media_fixture"] is True
    assert record["image_forensics_performed"] is False
