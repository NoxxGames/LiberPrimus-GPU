from test_stage5cm_common import load_yaml


def test_stage5cm_stage5bd_preservation_keeps_plan_ids_unchanged() -> None:
    payload = load_yaml("data/token-block/stage5cm-stage5bd-plan-preservation.yaml")
    assert payload["stage5bd_dry_run_records_remain_valid"] is True
    assert payload["stage5bd_run_plan_id_count"] == 10
    assert payload["stage5bd_run_plan_ids_changed"] is False
    assert payload["stage5bd_dry_run_plan_manifest_changed"] is False
    assert payload["stage5bd_plan_superseded"] is False
    assert payload["string4_added_to_stage5bd_run_plan_ids"] is False
    assert payload["string4_added_to_active_dry_run_inputs"] is False
