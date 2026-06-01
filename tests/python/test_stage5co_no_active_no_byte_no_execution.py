from libreprimus.token_block.stage5co import (
    validate_stage5co_actual_record_rejection,
    validate_stage5co_sidecar_gates,
)

from test_stage5co_common import load_yaml


def test_stage5co_no_active_no_byte_no_execution_gates_are_closed() -> None:
    assert load_yaml("data/token-block/stage5co-no-active-ingestion-proof.yaml")[
        "no_active_ingestion_status"
    ] == "closed"
    assert load_yaml("data/token-block/stage5co-no-byte-stream-transition-gate.yaml")[
        "no_byte_stream_transition_gate_status"
    ] == "closed"
    assert load_yaml("data/token-block/stage5co-no-execution-transition-gate.yaml")[
        "no_execution_transition_gate_status"
    ] == "closed"
    assert load_yaml("data/token-block/stage5co-manifest-supersession-nonactivation-proof.yaml")[
        "manifest_supersession_performed"
    ] is False

    counts, errors = validate_stage5co_sidecar_gates()
    assert errors == []
    assert counts["stage5co_sidecar_gates_valid"] is True


def test_stage5co_rejects_synthetic_byte_stream_execution_and_solve_claim() -> None:
    assert validate_stage5co_actual_record_rejection({"byte_stream_generation_authorized_now": True})
    assert validate_stage5co_actual_record_rejection({"execution_authorized_now": True})
    assert validate_stage5co_actual_record_rejection({"solve_claim": True})
