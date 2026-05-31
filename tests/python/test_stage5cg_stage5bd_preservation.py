from test_stage5cg_common import load_yaml


def test_stage5cg_preserves_stage5bd_run_plan_ids() -> None:
    payload = load_yaml("data/token-block/stage5cg-stage5bd-plan-preservation.yaml")
    assert payload["stage5bd_dry_run_records_remain_valid"] is True
    assert payload["stage5bd_run_plan_id_count"] == 10
    assert payload["stage5bd_run_plan_ids_changed"] is False
    assert payload["stage5bd_dry_run_plan_manifest_changed"] is False
