from test_stage5cy_common import ensure_stage5cy_built, load_yaml


def test_stage5cy_preserves_stage5cw_preflight_stage5cu_and_stage5cs() -> None:
    ensure_stage5cy_built()
    stage5cw = load_yaml("data/token-block/stage5cy-stage5cw-preservation.yaml")
    stage5cu = load_yaml("data/token-block/stage5cy-stage5cu-preservation.yaml")
    stage5cs = load_yaml("data/token-block/stage5cy-stage5cs-preservation.yaml")

    assert stage5cw["stage5cw_complete"] is True
    assert stage5cw["stage5cw_preserved_without_historical_edit"] is True
    assert stage5cw["stage5cw_real_decision_package_preflight_status_preserved"] == "review_preflight_only"
    assert stage5cw["stage5cw_pytest_count_warning_reconciled_by_stage5cy"] is True
    assert stage5cu["stage5cu_negative_fixture_count_preserved"] == 41
    assert stage5cu["stage5cu_real_decision_negative_fixture_count_preserved"] == 10
    assert stage5cu["stage5cu_option_selection_misuse_case_count_preserved"] == 13
    assert stage5cs["stage5cs_option_count_preserved"] == 6
    assert stage5cs["stage5cs_exact_option_set_preserved"] is True
    assert stage5cs["all_options_unselected"] is True


def test_stage5cy_preserves_stage5bd_and_active_lineage() -> None:
    ensure_stage5cy_built()
    stage5bd = load_yaml("data/token-block/stage5cy-stage5bd-plan-preservation.yaml")
    lineage = load_yaml("data/token-block/stage5cy-active-lineage-preservation.yaml")

    assert stage5bd["stage5bd_run_plan_id_count"] == 10
    assert stage5bd["stage5bd_run_plan_ids_changed"] is False
    assert stage5bd["stage5bd_dry_run_plan_manifest_changed"] is False
    assert stage5bd["stage5bd_plan_superseded"] is False
    assert lineage["active_lineage_record_count"] == 8
    assert lineage["correct_stage5aw_path_included"] is True
    assert lineage["deprecated_stage5aw_path_absent"] is True
    assert lineage["all_lineage_paths_resolve"] is True
