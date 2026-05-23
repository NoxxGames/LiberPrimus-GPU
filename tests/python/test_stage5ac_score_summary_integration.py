from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _record(path: str) -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"][0]


def test_stage5ac_score_summary_integration_is_stage4i_compatible() -> None:
    record = _record("data/cuda/stage5ac-prime-minus-one-cuda-synthetic-score-summary-integration.yaml")
    labels = {
        item["label"]
        for item in yaml.safe_load(Path("data/scoring/confidence-label-records-v0.yaml").read_text(encoding="utf-8"))[
            "records"
        ]
    }
    assert record["score_summary_contract"] == "stage4i"
    assert record["score_interpretation"] == "triage_only"
    assert record["confidence_label"] in labels
    assert record["confidence_label"] == "positive_control_like"
    assert record["scoring_model_added"] is False
    assert record["scorer_semantics_changed"] is False
    assert record["solve_claim"] is False
