from test_stage5ca_common import load_yaml


def test_stage5ca_active_lineage_uses_correct_stage5aw_path() -> None:
    lineage = load_yaml("data/token-block/stage5ca-active-lineage-preservation.yaml")
    paths = lineage["preserved_active_record_paths"]
    assert "data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml" in paths
    assert "data/token-block/stage5aw-repaired-branch-manifest.yaml" not in paths
    assert lineage["active_lineage_record_count"] == 8
    assert lineage["all_preserved_active_paths_resolve"] is True
