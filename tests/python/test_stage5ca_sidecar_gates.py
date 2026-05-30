from test_stage5ca_common import load_yaml


def test_stage5ca_no_active_ingestion_remains_closed() -> None:
    proof = load_yaml("data/token-block/stage5ca-no-active-ingestion-proof.yaml")
    assert proof["no_active_ingestion_status"] == "preserved_closed"
    assert proof["string4_sidecar_active"] is False
    assert proof["string4_active_input_allowed"] is False
    assert proof["string4_dry_run_ingestion_allowed_now"] is False
    assert proof["string4_added_to_active_dry_run_inputs"] is False


def test_stage5ca_no_byte_stream_proof_remains_closed() -> None:
    proof = load_yaml("data/token-block/stage5ca-no-byte-stream-proof.yaml")
    assert proof["no_byte_stream_gate_status"] == "closed"
    assert proof["string4_byte_stream_generation_allowed"] is False
    assert proof["real_byte_stream_generated"] is False
    assert proof["variant_byte_streams_generated"] is False
