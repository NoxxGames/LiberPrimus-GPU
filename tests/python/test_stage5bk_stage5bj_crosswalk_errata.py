from test_stage5bk_common import load_yaml


def test_stage5bk_records_stage5bj_hidden_image_errata_warning() -> None:
    payload = load_yaml("data/historical-route/stage5bk-stage5bj-crosswalk-review-and-errata.yaml")
    assert payload["stage5bj_crosswalk_errata_count"] == 1
    record = payload["records"][0]
    assert record["source_stage5bj_record_id"] == "stage5bj-page-body-hidden-original-image"
    assert record["supersedes_for_planning"] is True
    assert record["route_equivalent_file_is_page_body_snapshot"] is False
    assert record["route_equivalent_file_is_media_fixture"] is True
