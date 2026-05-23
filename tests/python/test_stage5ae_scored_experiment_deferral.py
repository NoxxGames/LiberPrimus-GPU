from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ae_scored_experiments_remain_deferred() -> None:
    record = yaml.safe_load(Path("data/cuda/stage5ae-corrected-bounded-p56-scored-experiment-deferral.yaml").read_text())["records"][0]
    assert record["deferral_status"] == "deferred_manifest_gate_required"
    assert record["scored_experiment_execution_allowed"] is False
    assert record["scored_experiment_executed"] is False
    assert record["benchmark_execution_allowed"] is False
