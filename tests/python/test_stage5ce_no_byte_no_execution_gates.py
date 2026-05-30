from pathlib import Path

import yaml

from libreprimus.token_block.stage5ce import (
    validate_stage5ce_no_byte_stream_transition_gate,
    validate_stage5ce_no_execution_transition_gate,
)
from test_stage5ce_common import load_yaml


def test_stage5ce_no_byte_stream_gate_closed() -> None:
    payload = load_yaml("data/token-block/stage5ce-no-byte-stream-transition-gate.yaml")
    assert payload["no_byte_stream_transition_gate_status"] == "closed"
    assert payload["byte_stream_generation_authorized_now"] is False
    assert payload["real_byte_stream_generated"] is False
    assert payload["variant_byte_streams_generated"] is False


def test_stage5ce_byte_stream_authorization_true_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5ce-no-byte-stream-transition-gate.yaml")
    payload["byte_stream_generation_authorized_now"] = True
    candidate = tmp_path / "byte_gate.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5ce_no_byte_stream_transition_gate(gate=candidate)
    assert counts["stage5ce_no_byte_stream_transition_gate_valid"] is False
    assert "byte_stream_generation_authorized_now must be false" in errors


def test_stage5ce_no_execution_gate_closed() -> None:
    payload = load_yaml("data/token-block/stage5ce-no-execution-transition-gate.yaml")
    assert payload["no_execution_transition_gate_status"] == "closed"
    assert payload["execution_authorized_now"] is False
    assert payload["token_block_experiment_executed"] is False
    assert payload["cuda_execution_performed"] is False


def test_stage5ce_execution_authorization_true_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5ce-no-execution-transition-gate.yaml")
    payload["execution_authorized_now"] = True
    candidate = tmp_path / "execution_gate.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5ce_no_execution_transition_gate(gate=candidate)
    assert counts["stage5ce_no_execution_transition_gate_valid"] is False
    assert "execution_authorized_now must be false" in errors
