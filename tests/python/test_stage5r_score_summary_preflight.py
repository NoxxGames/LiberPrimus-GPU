from __future__ import annotations

import yaml


def test_stage5r_score_summary_preflight_cites_stage4i_triage_only() -> None:
    records = yaml.safe_load(open("data/cuda/stage5r-gematria-expanded-solved-fixture-score-summary-preflight.yaml", encoding="utf-8"))[
        "records"
    ]
    assert len(records) == 3
    for record in records:
        assert record["score_summary_contract"] == "stage4i"
        assert record["score_interpretation"] == "triage_only"
        assert record["stage4i_confidence_labels_only"] is True
        assert record["score_status"] == "scoring_not_available"
        assert record["score_as_solve_evidence_allowed"] is False
        assert record["new_scorer_added"] is False
        assert record["method_status_upgrade_allowed"] is False
        assert record["stage5s_ready"] is True
