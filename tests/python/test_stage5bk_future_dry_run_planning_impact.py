from test_stage5bk_common import load_yaml


def test_stage5bk_future_dry_run_planning_impact_stays_no_byte_stream() -> None:
    payload = load_yaml("data/token-block/stage5bk-future-dry-run-planning-impact.yaml")
    assert payload["dry_run_plan_ids_remain_metadata_only"] is True
    assert payload["future_runner_must_cite_stage5bk_constraints"] is True
    assert payload["real_byte_stream_generated"] is False
    assert payload["variant_materialisation_performed"] is False
