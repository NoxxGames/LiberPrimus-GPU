from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _records(path: str) -> list[dict[str, Any]]:
    return list(yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"])


def test_scored_experiments_and_benchmarks_remain_deferred_or_blocked() -> None:
    records = _records("data/cuda/stage5ac-prime-minus-one-cuda-synthetic-scored-experiment-deferral.yaml")
    by_class = {record["experiment_class"]: record for record in records}
    assert by_class["bounded_cpu_native_scored_experiment"]["deferral_status"] == "deferred_manifest_gate_required"
    assert by_class["bounded_solved_fixture_score_regression"]["deferral_status"] == "deferred_manifest_gate_required"
    assert by_class["bounded_unsolved_page_micro_pilot"]["deferral_status"] == "blocked"
    assert by_class["cuda_scored_experiment"]["deferral_status"] == "blocked_pending_cuda_contract_and_parity"
    assert by_class["benchmark_experiment"]["deferral_status"] == "blocked_pending_benchmark_planning_stage"
    assert by_class["website_expansion"]["deferral_status"] == "deferred_future_unnumbered_project"
    assert all(record["execution_enabled"] is False for record in records)
    assert all(record["scored_experiment_executed"] is False for record in records)
    assert all(record["benchmark_execution_allowed"] is False for record in records)
