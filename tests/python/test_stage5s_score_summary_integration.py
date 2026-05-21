from __future__ import annotations

from pathlib import Path

import yaml


ALLOWED_LABELS = {
    "positive_control_like",
    "plausible_lead",
    "weak_lead",
    "noisy",
    "inconclusive",
    "garbage",
    "negative_control_like",
    "scoring_not_available",
    "calibration_not_available",
}


def _records(path: str) -> list[dict[str, object]]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"]


def test_stage5s_score_summary_records_use_stage4i_triage_contract() -> None:
    records = _records("data/cuda/stage5s-gematria-expanded-cuda-score-summary-integration.yaml")
    assert len(records) == 3
    for record in records:
        assert record["scorer_contract"] == "stage4i"
        assert record["confidence_label"] in ALLOWED_LABELS
        assert record["confidence_interpretation"] == "triage_only"
        assert record["score_or_label_status"] == "scoring_not_available"
        assert record["output_text_hash"] is None
        assert record["output_text_hash_status"] == "blocked_pending_transliteration_policy"
        assert record["solve_claim"] is False
        assert record["performance_claim"] is False
        assert record["speedup_claim"] is False
        assert record["method_status_upgrade_allowed"] is False


def test_stage5s_score_summary_records_do_not_rank_unsolved_candidates() -> None:
    records = _records("data/cuda/stage5s-gematria-expanded-cuda-score-summary-integration.yaml")
    for record in records:
        assert "rank" not in record
        assert record["unsolved_page_cuda_used"] is False
        assert record["does_not_validate_original_transform_family_semantics"] is True
