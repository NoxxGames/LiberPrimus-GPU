from test_stage5by_common import load_yaml


def test_stage5by_stage5bd_run_plan_ids_unchanged() -> None:
    preservation = load_yaml("data/token-block/stage5by-stage5bd-plan-preservation.yaml")
    assert preservation["stage5bd_run_plan_id_count_before"] == 10
    assert preservation["stage5bd_run_plan_id_count_after"] == 10
    assert preservation["stage5bd_run_plan_ids_changed"] is False
    assert preservation["stage5bd_dry_run_plan_manifest_changed"] is False


def test_stage5by_active_lineage_uses_correct_stage5aw_path() -> None:
    lineage = load_yaml("data/token-block/stage5by-active-lineage-preservation.yaml")
    paths = lineage["preserved_active_record_paths"]
    assert "data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml" in paths
    assert "data/token-block/stage5aw-repaired-branch-manifest.yaml" not in paths
    assert lineage["all_preserved_active_paths_resolve"] is True
