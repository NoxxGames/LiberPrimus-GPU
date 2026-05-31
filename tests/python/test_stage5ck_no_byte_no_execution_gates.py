from test_stage5ck_common import load_yaml


def test_no_byte_and_no_execution_gates_are_closed() -> None:
    byte_gate = load_yaml("data/token-block/stage5ck-no-byte-stream-transition-gate.yaml")
    execution_gate = load_yaml("data/token-block/stage5ck-no-execution-transition-gate.yaml")
    assert byte_gate["no_byte_stream_transition_gate_status"] == "closed"
    assert execution_gate["no_execution_transition_gate_status"] == "closed"
    assert byte_gate["byte_stream_generation_authorized_now"] is False
    assert byte_gate["real_byte_stream_generated"] is False
    assert execution_gate["execution_authorized_now"] is False
    assert execution_gate["token_block_experiment_executed"] is False
