from test_stage5bu_common import ROOT, load_yaml


def test_stage5bu_preserved_lineage_digest_index_covers_all_active_paths() -> None:
    digest = load_yaml("data/token-block/stage5bu-preserved-active-lineage-digest-index.yaml")

    assert digest["lineage_record_count"] == 8
    assert digest["all_lineage_paths_resolve"] is True
    assert digest["wrong_stage5aw_path_included"] is False
    assert digest["correct_stage5aw_path_included"] is True
    for row in digest["lineage_records"]:
        assert row["present"] is True
        assert row["sha256"]
        assert (ROOT / row["path"]).is_file()
