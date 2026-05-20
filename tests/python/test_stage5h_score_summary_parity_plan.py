from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5h_score_summary_plan_uses_stage4i_triage_labels() -> None:
    record = yaml.safe_load(Path("data/cuda/stage5h-gematria-score-summary-parity-plan.yaml").read_text(encoding="utf-8"))["records"][0]
    assert record["confidence_labels_triage_only"] is True
    assert "positive_control_like" in record["allowed_confidence_labels"]
    assert "solved" not in record["allowed_confidence_labels"]
    assert record["required_output_token_hash"] is True
