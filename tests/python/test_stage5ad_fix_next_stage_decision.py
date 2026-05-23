from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ad_fix_next_stage_selects_corrected_reporting() -> None:
    records = yaml.safe_load(Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-next-stage-decision.yaml").read_text())["records"]
    selected = [record for record in records if record["selected"] is True]

    assert len(selected) == 1
    assert selected[0]["option_id"] == "stage5ae_corrected_bounded_p56_cuda_formula_parity_reporting"
    assert "corrected bounded p56 CUDA formula parity reporting" in selected[0]["recommended_stage_title"]
    assert selected[0]["benchmark_execution_allowed"] is False
    assert selected[0]["scored_experiment_execution_allowed"] is False
