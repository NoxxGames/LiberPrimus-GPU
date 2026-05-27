from test_stage5bf_local_archive_location import load_yaml


def test_stage5bf_archive_tree_summary_counts_expected_local_archive_shape() -> None:
    payload = load_yaml("data/historical-route/stage5bf-archive-tree-summary.yaml")

    assert payload["archive_available"] is True
    assert payload["total_file_count"] == 1243
    assert payload["total_size_bytes"] == 838987564
    assert payload["file_count_by_extension"][".jpg"] == 520
    assert payload["expected_year_directories_present"]["2012"] is True
    assert payload["expected_year_directories_present"]["2017"] is True
    assert payload["archive_tree_digest"] == "bdc8739120be85fc7015e495704ee80bc80ef3a25cfc32c43e3b4d7de40270af"
