from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _record(path: str) -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"][0]


def test_stage5ac_result_store_integration_is_stage4p_compatible() -> None:
    record = _record("data/cuda/stage5ac-prime-minus-one-cuda-synthetic-result-store-integration.yaml")
    assert record["result_store_contract"] == "stage4p"
    assert record["stage4p_compatibility"] == "compatible"
    assert record["result_source_kind"] == "prime_minus_one_cuda_synthetic_parity_metadata"
    assert record["source_presence_status"] == "committed_summary_present"
    assert record["generated_outputs_committed"] is False
    assert record["generated_body_publication_allowed"] is False
    assert record["performance_claim_allowed"] is False
    assert record["speedup_claim_allowed"] is False
    assert record["solve_claim"] is False
