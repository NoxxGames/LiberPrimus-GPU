from test_stage5bu_common import load_yaml


def test_stage5bu_preserves_string4_gate_and_stage5bd_plan() -> None:
    gate = load_yaml("data/token-block/stage5bu-string4-gate-preservation.yaml")
    stage5bd = load_yaml("data/token-block/stage5bu-stage5bd-plan-preservation.yaml")
    no_active = load_yaml("data/token-block/stage5bu-no-active-ingestion-proof.yaml")

    assert gate["string4_gate_status"] == "closed"
    assert gate["string4_active_input_allowed"] is False
    assert gate["string4_dry_run_ingestion_allowed_now"] is False
    assert stage5bd["stage5bd_dry_run_plan_changed"] is False
    assert stage5bd["stage5bd_dry_run_records_changed"] is False
    assert no_active["real_byte_stream_generated"] is False
    assert no_active["cuda_execution_performed"] is False
