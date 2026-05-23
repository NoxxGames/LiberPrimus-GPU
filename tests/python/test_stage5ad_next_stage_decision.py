from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _records(path: str) -> list[dict[str, Any]]:
    return list(yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"])


def test_stage5ad_next_stage_selects_mismatch_investigation() -> None:
    records = _records("data/cuda/stage5ad-bounded-p56-cuda-next-stage-decision.yaml")
    selected = [record for record in records if record["selected"] is True]

    assert len(records) == 10
    assert len(selected) == 1
    assert selected[0]["option_id"] == "stage5ad_fix_bounded_p56_cuda_mismatch_investigation"
    assert selected[0]["recommended_prompt_type"] == "Codex"
    assert "mismatch" in selected[0]["recommended_stage_title"].lower()
    assert all(record["benchmark_execution_allowed"] is False for record in records)
    assert all(record["unsolved_page_scope_allowed"] is False for record in records)
