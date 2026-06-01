from test_stage5cs_common import ensure_stage5cs_built, load_yaml


def test_stage5cs_preserves_stage5bd_run_plan_ids() -> None:
    ensure_stage5cs_built()
    payload = load_yaml("data/token-block/stage5cs-stage5bd-plan-preservation.yaml")
    assert payload["stage5bd_run_plan_id_count"] == 10
    assert payload["stage5bd_run_plan_ids_changed"] is False
    assert payload["stage5bd_plan_superseded"] is False
