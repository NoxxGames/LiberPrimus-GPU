from __future__ import annotations

from libreprimus.token_block.stage5ee import validate_stage5ee_sidecar_gates
from test_stage5ee_common import ensure_stage5ee_built, load_yaml


def test_stage5ee_sidecar_gates_remain_closed() -> None:
    ensure_stage5ee_built()

    assert validate_stage5ee_sidecar_gates().validation_error_count == 0
    for path in (
        "data/token-block/stage5ee-no-active-ingestion-proof.yaml",
        "data/token-block/stage5ee-no-byte-stream-transition-proof.yaml",
        "data/token-block/stage5ee-no-token-block-execution-proof.yaml",
    ):
        payload = load_yaml(path)
        assert payload["gate_status"] == "closed"
        assert payload["execution_performed"] is False
        assert payload["solve_claim"] is False
