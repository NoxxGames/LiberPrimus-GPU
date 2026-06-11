from __future__ import annotations

from libreprimus.token_block.stage5ec import validate_stage5ec_sidecar_gates
from test_stage5ec_common import ensure_stage5ec_built, load_yaml


def test_stage5ec_sidecar_gates_remain_closed() -> None:
    ensure_stage5ec_built()

    assert validate_stage5ec_sidecar_gates().validation_error_count == 0
    for path in (
        "data/token-block/stage5ec-no-active-ingestion-proof.yaml",
        "data/token-block/stage5ec-no-byte-stream-transition-proof.yaml",
        "data/token-block/stage5ec-no-execution-transition-proof.yaml",
    ):
        payload = load_yaml(path)
        assert payload["gate_status"] == "closed"
        assert payload["execution_performed"] is False
        assert payload["solve_claim"] is False
