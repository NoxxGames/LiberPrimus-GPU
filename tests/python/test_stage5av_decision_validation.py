from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5av_decision_validation_counts_clean() -> None:
    validation = yaml.safe_load(
        (ROOT / "data/token-block/stage5av-decision-file-validation.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert validation["valid_for_stage5av_integration"] is True
    assert validation["validation_error_count"] == 0
    assert validation["validation_warning_count"] == 0
    assert validation["decision_counts"] == {"keep_current": 126, "unresolved": 77}
    assert validation["confidence_counts"] == {"high": 126, "medium": 77}
    assert validation["requires_second_review_counts"] == {"false": 126, "true": 77}
    assert validation["stage5at_token_case_255_selected_token"] == "1K"
