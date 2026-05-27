from pathlib import Path

import yaml


def test_stage5bd_guardrail_preserves_no_execution_boundary() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bd-guardrail.yaml").read_text())

    assert payload["real_token_block_byte_streams_generated"] is False
    assert payload["cuda_execution_performed"] is False
    assert payload["solve_claim"] is False
