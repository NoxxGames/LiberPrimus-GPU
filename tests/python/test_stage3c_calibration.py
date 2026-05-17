from __future__ import annotations

from pathlib import Path

from libreprimus.scoring.calibration import (
    build_control_record,
    classify_score,
    derive_thresholds,
    run_scoring_calibration,
)
from libreprimus.scoring.validation import validate_scoring_calibration_summary, validate_scoring_control_record


def _write_candidate_outputs(stage3a: Path, stage3b: Path) -> None:
    stage3a.mkdir(parents=True)
    (stage3b / "reverse_direction").mkdir(parents=True)
    noisy = (
        '{"output_normalized_text":"QXQXQXQXQXQXQXQXQXQX","transform_family":"affine_mod29",'
        '"transform_parameters":{"a":1,"b":2}}\n'
    )
    reverse = (
        '{"output_normalized_text":"JZJZJZJZJZJZJZJZJZJZ","transform_family":"affine_mod29_reverse",'
        '"transform_parameters":{"a":2,"b":3}}\n'
    )
    (stage3a / "top_candidates.jsonl").write_text(noisy, encoding="utf-8")
    (stage3b / "reranked_top_candidates.jsonl").write_text(noisy, encoding="utf-8")
    (stage3b / "reverse_direction" / "top_candidates.jsonl").write_text(reverse, encoding="utf-8")


def test_calibration_summary_validates_schema(tmp_path: Path) -> None:
    stage3a = tmp_path / "stage3a"
    stage3b = tmp_path / "stage3b"
    _write_candidate_outputs(stage3a, stage3b)

    result = run_scoring_calibration(stage3_results_dir=stage3a, stage3b_results_dir=stage3b, out_dir=tmp_path / "out", allow_warnings=True)

    validate_scoring_calibration_summary(result.summary)
    assert result.summary["solve_claim"] is False
    assert result.summary["positive_control_count"] >= 10
    assert result.summary["null_control_count"] == 250
    assert result.summary["candidate_count"] == 3


def test_confidence_labels_separate_readable_and_noisy_controls() -> None:
    positive = [build_control_record({"control_id": "pos", "source": "test", "text": "THE PATH OF WISDOM AND LIGHT"}, "positive", generated_at="now", cribs=[])]
    null = [build_control_record({"control_id": "null", "source": "test", "text": "QXQXJZJZQXQXJZJZ"}, "null", generated_at="now", cribs=[])]
    negative = [build_control_record({"control_id": "neg", "source": "test", "text": "AAAAAAAAAAAAAAAA"}, "negative", generated_at="now", cribs=[])]
    thresholds = derive_thresholds(positive, null, negative)
    positive_label = classify_score(positive[0]["score_summary"], positive[0]["crib_check"], thresholds)
    null_label = classify_score(null[0]["score_summary"], null[0]["crib_check"], thresholds)

    assert positive_label in {"positive_control_like", "plausible_lead", "weak_lead"}
    assert null_label in {"noisy", "garbage", "inconclusive"}
    validate_scoring_control_record(positive[0] | {"confidence_label": positive_label})
