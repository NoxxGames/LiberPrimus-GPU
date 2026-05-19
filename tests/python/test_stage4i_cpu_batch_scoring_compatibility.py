from __future__ import annotations

from libreprimus.scoring_consolidation.cpu_batch_integration import check_cpu_batch_summary, score_summary_from_cpu_batch_result
from libreprimus.scoring_consolidation.validation import validate_score_summary


def test_stage4i_cpu_batch_summary_is_compatible() -> None:
    payload = check_cpu_batch_summary("data/research/stage4h-cpu-batch-api-summary.yaml")
    assert payload["compatible"] is True
    assert payload["scoring_available_count"] == 6


def test_stage4i_cpu_batch_result_maps_to_score_summary_schema() -> None:
    record = {
        "candidate_id": "candidate-1",
        "input_stream_id": "stream-1",
        "transform_family": "direct_translation",
        "score_summary": {
            "score_status": "scored",
            "confidence_label": "lead",
            "total_score": 2.0,
            "length_normalized_score": 2.0,
            "no_solve_claim": True,
        },
    }
    summary = score_summary_from_cpu_batch_result(record)
    assert summary["confidence_label"] == "plausible_lead"
    validate_score_summary(summary)
