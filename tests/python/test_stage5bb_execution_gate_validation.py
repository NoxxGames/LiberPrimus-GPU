from pathlib import Path

import yaml


def test_stage5bb_execution_gate_validation_records_blocked_methods() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bb-execution-gate-validation.yaml").read_text())

    assert payload["validation_status"] == "passed"
    assert payload["execution_authorised_now"] is False
    assert payload["gate_enforcer_blocks_execution"] is True
    assert "generate_real_token_block_byte_stream" in payload["blocked_scaffold_methods"]
    assert "run_dwh_hash_search" in payload["blocked_scaffold_methods"]
