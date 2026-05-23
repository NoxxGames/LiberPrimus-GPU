from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _records(path: str) -> list[dict[str, Any]]:
    return list(yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"])


def test_stage5ad_result_store_preflight_blocks_mismatch_integration() -> None:
    record = _records("data/cuda/stage5ad-bounded-p56-cuda-result-store-preflight.yaml")[0]

    assert record["result_source_kind"] == "bounded_p56_cuda_parity"
    assert record["result_store_contract"] == "stage4p"
    assert record["preflight_status"] == "blocked_bounded_p56_cuda_hash_mismatch"
    assert record["compact_summary_only"] is True
    assert record["generated_outputs_committed"] is False
    assert record["solve_claim"] is False
