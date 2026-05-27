from pathlib import Path

import yaml


def test_stage5bd_execution_gate_validation_fails_closed() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bd-execution-gate-dry-run-validation.yaml").read_text())

    assert payload["gate_enforcer_blocks_execution"] is True
    assert payload["execution_authorised_now"] is False
    assert "generate_real_token_block_byte_stream" in payload["blocked_methods"]
    assert payload["validation_status"] == "passed"
