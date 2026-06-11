from __future__ import annotations

from test_stage5ea_common import ensure_stage5ea_built, load_yaml


def test_stage5ea_keeps_active_byte_and_execution_gates_closed() -> None:
    ensure_stage5ea_built()

    active = load_yaml("data/token-block/stage5ea-no-active-ingestion-proof.yaml")
    bytes_record = load_yaml("data/token-block/stage5ea-no-byte-stream-transition-proof.yaml")
    execution = load_yaml("data/token-block/stage5ea-no-execution-transition-proof.yaml")

    assert active["active_ingestion_gate_closed"] is True
    assert bytes_record["byte_stream_transition_gate_closed"] is True
    assert execution["execution_transition_gate_closed"] is True
    assert execution["execution_performed"] is False
    assert execution["solve_claim"] is False
