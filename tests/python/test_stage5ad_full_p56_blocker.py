from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _records(path: str) -> list[dict[str, Any]]:
    return list(yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"])


def test_stage5ad_full_p56_remains_blocked() -> None:
    record = _records("data/cuda/stage5ad-bounded-p56-cuda-full-p56-blocker.yaml")[0]

    assert record["full_p56_status"] == "blocked_full_p56_token_buffer_missing"
    assert record["full_p56_cuda_execution_allowed"] is False
    assert record["full_p56_generated_body_publication_allowed"] is False
    assert record["full_token_buffer_committed"] is False
    assert record["solve_claim"] is False
