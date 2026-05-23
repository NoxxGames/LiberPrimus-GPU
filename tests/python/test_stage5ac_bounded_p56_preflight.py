from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

EXPECTED_HASH = "4a3059f12c0f8450bd4ef7e31bf879fbc104202e5fb0e53b7ba514241f07cd87"


def _record(path: str) -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"][0]


def test_bounded_p56_is_preflighted_but_not_executed() -> None:
    record = _record("data/cuda/stage5ac-bounded-p56-cuda-parity-preflight.yaml")
    assert record["bounded_p56_vector_id"] == "stage5z-validation-p56-bounded-v0"
    assert record["mapping_id"] == "stage5w-mapping-p56-stage4o-bounded-v0"
    assert record["expected_output_token_hash"] == EXPECTED_HASH
    assert record["preflight_status"] == "ready_for_stage5ad_bounded_p56_cuda_parity"
    assert record["bounded_p56_cuda_execution_allowed_current_stage"] is False
    assert record["bounded_p56_cuda_execution_ready_next_stage"] is True
    assert record["requires_explicit_future_stage"] is True
    assert record["cuda_execution_performed"] is False
    assert record["benchmark_allowed"] is False
    assert record["scored_experiment_allowed"] is False
    assert record["unsolved_page_cuda_allowed"] is False
