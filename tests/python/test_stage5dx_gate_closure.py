from __future__ import annotations

from test_stage5dx_common import ensure_stage5dx_built, load_yaml


FALSE_FIELDS = [
    "historical_source_lock_records_rewritten",
    "number_fact_backfill_performed_now",
    "target_priority_decision_created_now",
    "pivot_target_selected_now",
    "route_extraction_performed_now",
    "byte_stream_generation_authorized_now",
    "real_byte_stream_generated",
    "execution_performed",
    "token_block_experiment_executed",
    "ocr_performed",
    "image_forensics_performed",
    "audio_stego_performed",
    "cuda_execution_performed",
    "scoring_performed",
    "solve_claim",
]


def test_stage5dx_summary_keeps_execution_and_solve_gates_closed() -> None:
    ensure_stage5dx_built()
    summary = load_yaml("data/project-state/stage5dx-summary.yaml")

    for field in FALSE_FIELDS:
        assert summary[field] is False
    assert summary["source_lock_entry_batch_review_performed_now"] is True
    assert summary["number_fact_review_batch_2_performed_now"] is True


def test_stage5dx_closed_gate_records_exist() -> None:
    ensure_stage5dx_built()

    for path in [
        "data/token-block/stage5dx-no-active-ingestion-proof.yaml",
        "data/token-block/stage5dx-no-byte-stream-transition-proof.yaml",
        "data/token-block/stage5dx-no-token-block-execution-proof.yaml",
    ]:
        payload = load_yaml(path)
        assert payload["gate_status"] == "closed"
        assert payload["execution_performed"] is False
        assert payload["solve_claim"] is False
