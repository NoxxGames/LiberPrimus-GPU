from test_stage5bk_common import load_yaml


def test_stage5bk_tree_summary_records_digest_and_count() -> None:
    payload = load_yaml("data/historical-route/stage5bk-iddqd-v2-tree-summary.yaml")
    assert payload["source_root_found"] is True
    assert payload["total_file_count"] == 309
    assert len(payload["tree_digest"]) == 64
    assert payload["raw_iddqd_v2_files_committed"] is False
