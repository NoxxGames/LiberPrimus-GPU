from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _record(path: str) -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"][0]


def test_full_p56_remains_blocked() -> None:
    record = _record("data/cuda/stage5ac-prime-minus-one-cuda-synthetic-full-p56-blocker.yaml")
    assert record["full_p56_status"] == "blocked_full_p56_token_buffer_missing"
    assert record["full_p56_cuda_execution_allowed"] is False
    assert record["full_p56_native_execution_allowed"] is False
    assert record["full_p56_generated_body_publication_allowed"] is False
    assert "full_committed_p56_cipher_token_buffer" in record["blocker_reason"]
    assert record["solve_claim"] is False
