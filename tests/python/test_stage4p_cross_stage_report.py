from __future__ import annotations

import json
from pathlib import Path

from libreprimus.result_store.cross_stage_report import build_cross_stage_report


def test_cross_stage_report_counts_are_deterministic(tmp_path: Path) -> None:
    source = tmp_path / "cpu.jsonl"
    source.write_text(json.dumps(_cpu_result()) + "\n", encoding="utf-8")
    manifest = _manifest(tmp_path, source)
    first = build_cross_stage_report(manifest, out_dir=tmp_path / "one", summary_out=tmp_path / "one.yaml")
    second = build_cross_stage_report(manifest, out_dir=tmp_path / "two", summary_out=tmp_path / "two.yaml")
    assert first["source_inventory_records"] == second["source_inventory_records"] == 2
    assert first["unified_result_records"] == second["unified_result_records"] == 2
    assert first["confidence_label_counts"] == second["confidence_label_counts"]
    assert first["generated_outputs_committed"] is False


def _cpu_result() -> dict:
    return {
        "record_type": "cpu_batch_result_record",
        "candidate_id": "candidate",
        "input_stream_id": "stream",
        "transform_family": "direct_translation",
        "output_token_hash": "1" * 64,
        "score_summary": {
            "score_status": "scored",
            "confidence_label": "plausible_lead",
            "length_normalized_score": 1.0,
        },
    }


def _manifest(tmp_path: Path, source: Path) -> Path:
    manifest = tmp_path / "manifest.yaml"
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
  - source_id: cpu
    source_stage_id: stage-test
    result_source_kind: cpu_batch_result
    source_path: {source}
    optional_generated: true
    method_family: cpu_batch_transform_api
    source_record_type: cpu_batch_result_record
  - source_id: raw
    source_stage_id: stage-test
    result_source_kind: bounded_experiment_summary
    source_path: data/raw/example.txt
    raw_required: true
    method_family: unknown
""",
        encoding="utf-8",
    )
    return manifest
