from __future__ import annotations

from libreprimus.token_block.stage5dz import PROJECT_STATE_PATHS, TOKEN_PATHS
from test_stage5dz_common import ensure_stage5dz_built, load_yaml


def test_stage5dz_execution_and_batch3_gates_remain_closed() -> None:
    ensure_stage5dz_built()

    summary = load_yaml(PROJECT_STATE_PATHS["summary"])

    for key in (
        "number_fact_review_batch_3_performed_now",
        "target_priority_decision_created_now",
        "pivot_target_selected_now",
        "route_extraction_performed_now",
        "triangle_route_extraction_performed_now",
        "page32_route_extraction_performed_now",
        "byte_stream_generation_authorized_now",
        "variant_byte_streams_generated",
        "execution_performed",
        "image_forensics_performed",
        "ocr_performed",
        "target_class_validation_implemented",
        "historical_source_lock_records_rewritten",
        "solve_claim",
    ):
        assert summary[key] is False
    assert load_yaml(TOKEN_PATHS["no_active_ingestion_proof"])["gate_status"] == "closed"
    assert load_yaml(TOKEN_PATHS["no_byte_stream_transition_proof"])["gate_status"] == "closed"
    assert load_yaml(TOKEN_PATHS["no_execution_transition_proof"])["gate_status"] == "closed"
