from __future__ import annotations

import json
from pathlib import Path

from libreprimus.result_store.normalization import build_unified_result_records


def test_unified_result_records_include_output_hashes(tmp_path: Path) -> None:
    source = tmp_path / "cpu.jsonl"
    source.write_text(json.dumps(_cpu_result()) + "\n", encoding="utf-8")
    manifest = _manifest(tmp_path, source)
    _, records, _ = build_unified_result_records(manifest, out_dir=tmp_path / "out")
    assert len(records) == 1
    assert records[0]["output_token_hash"] == "1" * 64
    assert records[0]["output_text_hash"] == "2" * 64
    assert records[0]["solve_claim"] is False
    assert records[0]["cuda_used"] is False


def _cpu_result() -> dict:
    return {
        "record_type": "cpu_batch_result_record",
        "candidate_id": "candidate",
        "input_stream_id": "stream",
        "transform_family": "direct_translation",
        "output_token_hash": "1" * 64,
        "output_text_hash": "2" * 64,
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
""",
        encoding="utf-8",
    )
    return manifest
