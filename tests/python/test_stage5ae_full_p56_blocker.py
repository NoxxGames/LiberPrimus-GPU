from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ae_full_p56_remains_blocked() -> None:
    record = yaml.safe_load(Path("data/cuda/stage5ae-corrected-bounded-p56-full-p56-blocker.yaml").read_text())["records"][0]
    assert record["full_p56_status"] == "blocked_full_p56_token_buffer_missing"
    assert record["full_p56_cuda_allowed"] is False
    assert record["full_p56_cuda_executed"] is False
    assert record["unsolved_page_cuda_allowed"] is False
