from libreprimus.token_block.stage5ci import validate_stage5ci_sidecar_gates
from test_stage5ci_common import load_yaml, write_yaml


def test_stage5ci_no_byte_and_no_execution_gates_closed(tmp_path) -> None:
    counts, errors = validate_stage5ci_sidecar_gates()
    assert not errors
    assert counts["no_byte_stream_transition_gate_status"] == "closed"
    assert counts["no_execution_transition_gate_status"] == "closed"

    payload = load_yaml("data/token-block/stage5ci-no-byte-stream-transition-gate.yaml")
    payload["byte_stream_generation_authorized_now"] = True
    bad = tmp_path / "byte.yaml"
    write_yaml(bad, payload)

    _, bad_errors = validate_stage5ci_sidecar_gates(no_byte_stream_transition_gate=bad)
    assert bad_errors


def test_stage5ci_execution_authorization_fails(tmp_path) -> None:
    payload = load_yaml("data/token-block/stage5ci-no-execution-transition-gate.yaml")
    payload["execution_authorized_now"] = True
    bad = tmp_path / "execution.yaml"
    write_yaml(bad, payload)

    _, bad_errors = validate_stage5ci_sidecar_gates(no_execution_transition_gate=bad)
    assert bad_errors
