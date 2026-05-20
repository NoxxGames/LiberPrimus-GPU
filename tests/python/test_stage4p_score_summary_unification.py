from __future__ import annotations

import json
from pathlib import Path

from libreprimus.result_store.score_summary_unification import build_unified_score_summaries


def test_score_summary_unification_maps_cpu_batch_scores(tmp_path: Path) -> None:
    source = tmp_path / "cpu.jsonl"
    source.write_text(json.dumps(_cpu_result()) + "\n", encoding="utf-8")
    scores, _ = build_unified_score_summaries(_manifest(tmp_path, source), out_dir=tmp_path / "out")
    assert scores[0]["score_status"] == "scored"
    assert scores[0]["confidence_label"] == "plausible_lead"
    assert scores[0]["score_interpretation"] == "triage_only"


def test_unknown_score_semantics_become_unavailable(tmp_path: Path) -> None:
    source = tmp_path / "summary.json"
    source.write_text(json.dumps({"record_type": "summary"}), encoding="utf-8")
    scores, _ = build_unified_score_summaries(_manifest(tmp_path, source), out_dir=tmp_path / "out")
    assert scores[0]["score_status"] == "scoring_not_available"
    assert scores[0]["warnings"]


def _cpu_result() -> dict:
    return {
        "record_type": "cpu_batch_result_record",
        "candidate_id": "candidate",
        "input_stream_id": "stream",
        "transform_family": "direct_translation",
        "score_summary": {
            "score_status": "scored",
            "confidence_label": "plausible_lead",
            "length_normalized_score": 1.0,
        },
    }


def _manifest(tmp_path: Path, source: Path) -> Path:
    manifest = tmp_path / "manifest.yaml"
    suffix = "cpu_batch_result_record" if source.suffix == ".jsonl" else "summary"
    manifest.write_text(
        f"""
record_type: result_store_unification_manifest
cpu_only: true
cuda_used: false
cuda_required: false
no_solve_claim: true
canonical_corpus_active: false
page_boundaries_final: false
generated_outputs_committed: false
raw_data_processed: false
new_experiment_executed: false
new_scorer_added: false
sources:
  - source_id: source
    source_stage_id: stage-test
    result_source_kind: cpu_batch_result
    source_path: {source}
    optional_generated: true
    method_family: cpu_batch_transform_api
    source_record_type: {suffix}
""",
        encoding="utf-8",
    )
    return manifest
