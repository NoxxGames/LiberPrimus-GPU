from test_stage5cw_common import ensure_stage5cw_built, load_yaml


def test_stage5cw_transition_gates_remain_closed() -> None:
    ensure_stage5cw_built()
    no_active = load_yaml("data/token-block/stage5cw-no-active-ingestion-proof.yaml")
    no_byte = load_yaml("data/token-block/stage5cw-no-byte-stream-transition-gate.yaml")
    no_execution = load_yaml("data/token-block/stage5cw-no-execution-transition-gate.yaml")

    assert no_active["no_active_ingestion_status"] == "closed"
    assert no_active["string4_active_input_allowed"] is False
    assert no_active["active_manifest_registry_updated"] is False
    assert no_byte["no_byte_stream_transition_gate_status"] == "closed"
    assert no_byte["byte_stream_generation_authorized_now"] is False
    assert no_byte["real_decision_package_preflight_authorizes_bytes"] is False
    assert no_execution["no_execution_transition_gate_status"] == "closed"
    assert no_execution["execution_authorized_now"] is False
    assert no_execution["token_block_experiment_executed"] is False
    assert no_execution["real_decision_package_preflight_authorizes_execution"] is False
