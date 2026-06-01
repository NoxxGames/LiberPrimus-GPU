from libreprimus.token_block.stage5cq import (
    validate_stage5cq_actual_record_rejection,
    validate_stage5cq_sidecar_gates,
)

from test_stage5cq_common import ensure_stage5cq_built, load_yaml


def test_stage5cq_no_active_no_byte_no_execution_gates_are_closed() -> None:
    ensure_stage5cq_built()
    assert load_yaml("data/token-block/stage5cq-no-active-ingestion-proof.yaml")[
        "no_active_ingestion_status"
    ] == "closed"
    assert load_yaml("data/token-block/stage5cq-no-byte-stream-transition-gate.yaml")[
        "no_byte_stream_transition_gate_status"
    ] == "closed"
    assert load_yaml("data/token-block/stage5cq-no-execution-transition-gate.yaml")[
        "no_execution_transition_gate_status"
    ] == "closed"
    counts, errors = validate_stage5cq_sidecar_gates()
    assert not errors
    assert counts["stage5cq_sidecar_gates_valid"] is True


def test_stage5cq_rejects_byte_stream_execution_and_solve_claim() -> None:
    assert validate_stage5cq_actual_record_rejection({"byte_stream_generation_authorized_now": True})
    assert validate_stage5cq_actual_record_rejection({"execution_authorized_now": True})
    assert validate_stage5cq_actual_record_rejection({"solve_claim": True})
