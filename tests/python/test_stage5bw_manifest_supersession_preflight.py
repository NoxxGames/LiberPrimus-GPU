from test_stage5bw_common import load_yaml


def test_stage5bw_manifest_supersession_is_preflight_only() -> None:
    preflight = load_yaml("data/token-block/stage5bw-manifest-supersession-preflight.yaml")

    assert preflight["manifest_supersession_preflight_status"] == "proposed_only"
    assert preflight["manifest_supersession_performed"] is False
    assert preflight["current_active_records_preserved"] is True
    assert all(record["superseded_now"] is False for record in preflight["records"])


def test_stage5bw_stage5bd_run_plan_ids_remain_unchanged() -> None:
    preservation = load_yaml("data/token-block/stage5bw-stage5bd-plan-preservation.yaml")
    registry = load_yaml("data/token-block/stage5bd-run-plan-id-registry.yaml")

    assert preservation["stage5bd_run_plan_id_count_before"] == registry["run_plan_id_count"]
    assert preservation["stage5bd_run_plan_id_count_after"] == registry["run_plan_id_count"]
    assert preservation["stage5bd_run_plan_ids_changed"] is False
    assert preservation["string4_added_to_stage5bd_run_plan_ids"] is False
