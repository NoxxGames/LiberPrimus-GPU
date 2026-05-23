from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _records(path: str) -> list[dict[str, Any]]:
    return list(yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"])


def test_stage5ad_score_summary_preflight_uses_triage_only_no_score() -> None:
    record = _records("data/cuda/stage5ad-bounded-p56-cuda-score-summary-preflight.yaml")[0]

    assert record["score_summary_contract"] == "stage4i"
    assert record["confidence_label"] == "scoring_not_available"
    assert record["confidence_interpretation"] == "triage_only"
    assert record["score_status"] == "scoring_not_available"
    assert record["method_status_upgrade_allowed"] is False
    assert record["performance_claim_allowed"] is False
