from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _records(path: str) -> list[dict[str, Any]]:
    return list(yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"])


def test_stage5ad_scored_and_adjacent_experiment_deferrals_block_execution() -> None:
    records = _records("data/cuda/stage5ad-bounded-p56-cuda-scored-experiment-deferral.yaml")
    classes = {record["experiment_class"] for record in records}

    assert len(records) == 7
    assert "cuda_scored_experiment" in classes
    assert "benchmark_experiment" in classes
    assert "website_expansion" in classes
    assert "visual_clue_deep_research" in classes
    assert all(record["execution_enabled"] is False for record in records)
    assert all(record["scored_experiment_execution_allowed"] is False for record in records)
    assert all(record["benchmark_execution_allowed"] is False for record in records)
