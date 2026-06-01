from test_stage5cq_common import ensure_stage5cq_built, load_yaml


def test_stage5cq_stage5bd_preservation_keeps_plan_ids_unchanged() -> None:
    ensure_stage5cq_built()
    payload = load_yaml("data/token-block/stage5cq-stage5bd-plan-preservation.yaml")
    assert payload["stage5bd_run_plan_id_count"] == 10
    assert payload["stage5bd_run_plan_ids_changed"] is False
    assert payload["stage5bd_dry_run_plan_manifest_changed"] is False
    assert payload["stage5bd_plan_superseded"] is False
