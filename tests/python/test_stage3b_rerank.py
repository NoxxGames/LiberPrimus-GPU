from __future__ import annotations

from libreprimus.candidate_inspection.analysis import rerank_candidates


def _record(index: int, text: str, old_score: float) -> dict:
    return {
        "record_type": "bounded_candidate_record",
        "run_id": "synthetic",
        "queue_item_id": "synthetic",
        "transform_family": "test",
        "transform_parameters": {"i": index},
        "candidate_index": index,
        "input_slice_id": "synthetic",
        "output_normalized_text": text,
        "output_sha256": f"{index}" * 64,
        "score_summary": {"total_score": old_score, "common_word_hit_count": 0, "latin_letter_count": len(text), "entropy": 1.0},
        "ranking_features": {},
    }


def test_rerank_changes_order_when_refined_scores_differ() -> None:
    records = [
        _record(0, "QXQXQXQXQX", 99.0),
        _record(1, "THE AND WE CAN", 1.0),
    ]

    reranked = rerank_candidates(records)

    assert reranked[0]["candidate_index"] == 1
    assert reranked[0]["score_summary"]["confidence_label"] in {"lead", "weak_lead", "noisy"}
    assert reranked[-1]["score_summary"]["confidence_label"] == "garbage"
