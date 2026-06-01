from libreprimus.token_block.stage5cs import validate_stage5cs_sidecar_gates

from test_stage5cs_common import ensure_stage5cs_built, load_yaml


def test_stage5cs_no_active_no_byte_no_execution_gates_closed() -> None:
    ensure_stage5cs_built()
    active = load_yaml("data/token-block/stage5cs-no-active-ingestion-proof.yaml")
    byte = load_yaml("data/token-block/stage5cs-no-byte-stream-transition-gate.yaml")
    execution = load_yaml("data/token-block/stage5cs-no-execution-transition-gate.yaml")
    assert active["no_active_ingestion_status"] == "closed"
    assert byte["byte_stream_generation_authorized_now"] is False
    assert execution["execution_authorized_now"] is False
    counts, errors = validate_stage5cs_sidecar_gates()
    assert not errors
    assert counts["stage5cs_sidecar_gates_valid"] is True
