from __future__ import annotations

import json
from pathlib import Path

from libreprimus.candidate_inspection.analysis import inspect_results
from libreprimus.candidate_inspection.loader import load_candidate_records
from libreprimus.candidate_inspection.report import write_inspection_markdown


def _write_stage_outputs(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    records = [
        {
            "record_type": "bounded_candidate_record",
            "run_id": "synthetic-run",
            "queue_item_id": "synthetic-item",
            "transform_family": "caesar_shift_mod29",
            "transform_parameters": {"shift": 1},
            "candidate_index": 0,
            "input_slice_id": "synthetic",
            "output_normalized_text": "THE AND WE CAN",
            "output_sha256": "a" * 64,
            "score_summary": {"total_score": 10.0, "vowel_ratio": 0.35, "common_word_hit_count": 4, "common_word_hits": ["THE"], "entropy": 2.0},
            "ranking_features": {},
        },
        {
            "record_type": "bounded_candidate_record",
            "run_id": "synthetic-run",
            "queue_item_id": "synthetic-item",
            "transform_family": "affine_mod29",
            "transform_parameters": {"a": 2, "b": 3},
            "candidate_index": 1,
            "input_slice_id": "synthetic",
            "output_normalized_text": "QXQXQXQX",
            "output_sha256": "b" * 64,
            "score_summary": {"total_score": 1.0, "vowel_ratio": 0.0, "common_word_hit_count": 0, "common_word_hits": [], "entropy": 1.0},
            "ranking_features": {},
        },
    ]
    (path / "candidate_records.jsonl").write_text("\n".join(json.dumps(record) for record in records) + "\n", encoding="utf-8")
    (path / "top_candidates.jsonl").write_text(json.dumps(records[0]) + "\n" + json.dumps(records[1]) + "\n", encoding="utf-8")
    (path / "summary.json").write_text(json.dumps({"run_id": "synthetic-run"}), encoding="utf-8")


def test_candidate_loader_reads_synthetic_candidate_records(tmp_path: Path) -> None:
    _write_stage_outputs(tmp_path)

    records = load_candidate_records(tmp_path)

    assert len(records) == 2
    assert records[0]["transform_family"] == "caesar_shift_mod29"


def test_inspection_summary_groups_by_transform_and_scores(tmp_path: Path) -> None:
    _write_stage_outputs(tmp_path)

    summary = inspect_results(tmp_path, top_n=2, rerank=True)

    assert summary.transform_family_counts == {"caesar_shift_mod29": 1, "affine_mod29": 1}
    assert summary.score_distribution["max"] == 10.0
    assert summary.refined_top_candidate is not None


def test_inspection_markdown_omits_full_candidate_dump(tmp_path: Path) -> None:
    _write_stage_outputs(tmp_path)
    summary = inspect_results(tmp_path, top_n=2, rerank=True)
    report = write_inspection_markdown(tmp_path / "report.md", summary)
    text = report.read_text(encoding="utf-8")

    assert "output_normalized_text" not in text
    assert "THE AND WE CAN" not in text
    assert "Solve claim: false" in text
