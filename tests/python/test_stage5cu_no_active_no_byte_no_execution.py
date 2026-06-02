from libreprimus.token_block.stage5cu import validate_stage5cu_sidecar_gates

from test_stage5cu_common import ensure_stage5cu_built, load_yaml


def test_stage5cu_no_active_no_byte_no_execution_gates_closed() -> None:
    ensure_stage5cu_built()
    active = load_yaml("data/token-block/stage5cu-no-active-ingestion-proof.yaml")
    byte = load_yaml("data/token-block/stage5cu-no-byte-stream-transition-gate.yaml")
    execution = load_yaml("data/token-block/stage5cu-no-execution-transition-gate.yaml")
    assert active["string4_active_input_allowed"] is False
    assert byte["byte_stream_generation_authorized_now"] is False
    assert execution["execution_authorized_now"] is False
    assert execution["dwh_hash_search_performed"] is False
    assert execution["cuda_execution_performed"] is False
    counts, errors = validate_stage5cu_sidecar_gates()
    assert not errors
    assert counts["stage5cu_sidecar_gates_valid"] is True
