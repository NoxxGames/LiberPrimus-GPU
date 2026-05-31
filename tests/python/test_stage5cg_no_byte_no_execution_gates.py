from libreprimus.token_block.stage5cg import (
    validate_stage5cg_no_byte_stream_transition_gate,
    validate_stage5cg_no_execution_transition_gate,
)
from test_stage5cg_common import load_yaml, write_yaml


def test_stage5cg_no_byte_stream_gate_stays_closed(tmp_path) -> None:
    counts, errors = validate_stage5cg_no_byte_stream_transition_gate()
    assert not errors
    assert counts["no_byte_stream_transition_gate_status"] == "closed"

    payload = load_yaml("data/token-block/stage5cg-no-byte-stream-transition-gate.yaml")
    payload["byte_stream_generation_authorized_now"] = True
    bad = tmp_path / "byte.yaml"
    write_yaml(bad, payload)

    _, bad_errors = validate_stage5cg_no_byte_stream_transition_gate(gate=bad)
    assert bad_errors


def test_stage5cg_no_execution_gate_stays_closed(tmp_path) -> None:
    counts, errors = validate_stage5cg_no_execution_transition_gate()
    assert not errors
    assert counts["no_execution_transition_gate_status"] == "closed"

    payload = load_yaml("data/token-block/stage5cg-no-execution-transition-gate.yaml")
    payload["execution_authorized_now"] = True
    bad = tmp_path / "execution.yaml"
    write_yaml(bad, payload)

    _, bad_errors = validate_stage5cg_no_execution_transition_gate(gate=bad)
    assert bad_errors
