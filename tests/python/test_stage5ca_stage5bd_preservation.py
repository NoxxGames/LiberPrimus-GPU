from test_stage5ca_common import load_yaml


def test_stage5ca_stage5bd_run_plan_ids_unchanged() -> None:
    preservation = load_yaml("data/token-block/stage5ca-stage5bd-plan-preservation.yaml")
    assert preservation["stage5bd_plan_preservation_status"] == "preserved_unchanged"
    assert preservation["stage5bd_run_plan_id_count_before"] == 10
    assert preservation["stage5bd_run_plan_id_count_after"] == 10
    assert preservation["stage5bd_run_plan_ids_changed"] is False
    assert preservation["stage5bd_dry_run_records_remain_valid"] is True
