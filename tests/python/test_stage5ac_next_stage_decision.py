from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _records(path: str) -> list[dict[str, Any]]:
    return list(yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"])


def test_next_stage_decision_is_deterministic_and_bounded() -> None:
    records = _records("data/cuda/stage5ac-prime-minus-one-cuda-synthetic-next-stage-decision.yaml")
    selected = [record for record in records if record["selected"] is True]
    assert len(selected) == 1
    assert selected[0]["option_id"] == "stage5ad_bounded_p56_cuda_parity_run"
    assert selected[0]["recommended_stage_title"] == "Stage 5AD - bounded p56 CUDA parity run"
    assert selected[0]["future_cuda_execution_allowed"] is True
    assert selected[0]["unsolved_page_scope_allowed"] is False
    assert selected[0]["benchmark_execution_allowed"] is False
    assert selected[0]["scored_experiment_execution_allowed"] is False
    assert selected[0]["generated_body_publication_allowed"] is False
    assert all(record["cuda_execution_allowed_current_stage"] is False for record in records)
    assert all(record["cuda_source_changes_allowed_current_stage"] is False for record in records)
    assert all(record["method_status_upgrade_allowed"] is False for record in records)
