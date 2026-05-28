from test_stage5bm_common import load_yaml


def test_stage5bm_future_dry_run_planning_is_constraints_only() -> None:
    record = load_yaml("data/token-block/stage5bm-future-dry-run-planning-impact.yaml")

    assert record["future_dry_run_planning_impact_status"] == "metadata_constraints_only"
    assert "raw String 4 hex body" in record["future_dry_run_must_not_consume"]
    assert record["future_runner_must_cite_stage5bm_constraints"] is True
    assert record["execution_gate_default"] == "blocked"
    assert record["real_byte_stream_generated"] is False
