from libreprimus.token_block.stage5cm import validate_stage5cm_sidecar_gates

from test_stage5cm_common import load_yaml


def test_stage5cm_sidecar_no_byte_and_no_execution_gates_remain_closed() -> None:
    no_active = load_yaml("data/token-block/stage5cm-no-active-ingestion-proof.yaml")
    no_byte = load_yaml("data/token-block/stage5cm-no-byte-stream-transition-gate.yaml")
    no_execution = load_yaml("data/token-block/stage5cm-no-execution-transition-gate.yaml")
    sidecar = load_yaml("data/token-block/stage5cm-sidecar-activation-blocker.yaml")

    assert no_active["string4_sidecar_status"] == "scaffolded_inactive"
    assert sidecar["string4_sidecar_active"] is False
    assert no_byte["no_byte_stream_transition_gate_status"] == "closed"
    assert no_execution["no_execution_transition_gate_status"] == "closed"
    assert no_byte["byte_stream_generation_authorized_now"] is False
    assert no_execution["execution_authorized_now"] is False

    counts, errors = validate_stage5cm_sidecar_gates()
    assert errors == []
    assert counts["string4_sidecar_status"] == "scaffolded_inactive"
