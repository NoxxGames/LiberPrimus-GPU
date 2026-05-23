from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ae_score_summary_uses_stage4i_triage_shape_without_scoring() -> None:
    record = yaml.safe_load(Path("data/cuda/stage5ae-corrected-bounded-p56-score-summary-integration.yaml").read_text())["records"][0]
    assert record["score_summary_contract"] == "stage4i"
    assert record["score_status"] == "scoring_not_available"
    assert record["confidence_label"] == "scoring_not_available"
    assert record["score_interpretation"] == "triage_only"
    assert record["scored_experiment_executed"] is False
