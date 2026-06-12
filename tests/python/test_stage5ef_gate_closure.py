from __future__ import annotations

from libreprimus.token_block import stage5ef
from test_stage5ef_common import ensure_stage5ef_built, load_yaml


def test_stage5ef_sidecar_and_execution_gates_remain_closed() -> None:
    ensure_stage5ef_built()

    result = stage5ef.validate_stage5ef_sidecar_gates()
    summary = load_yaml("data/project-state/stage5ef-summary.yaml")

    assert result.validation_error_count == 0
    for key in [
        "new_source_lock_evidence_added_now",
        "number_fact_enrichment_overlays_added_now",
        "number_fact_backfill_performed_now",
        "target_priority_decision_created_now",
        "route_extraction_performed_now",
        "real_byte_stream_generated",
        "execution_performed",
        "cuda_execution_performed",
        "solve_claim",
    ]:
        assert summary[key] is False
