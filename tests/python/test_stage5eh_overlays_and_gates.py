from __future__ import annotations

from libreprimus.token_block import stage5eh
from test_stage5eh_common import stage5eh_data


def test_stage5eh_overlays_are_overlay_only() -> None:
    payload = stage5eh_data("overlay_collection")

    assert payload["overlay_count"] == 36
    assert len(payload["overlays"]) == 36
    for overlay in payload["overlays"]:
        assert overlay["review_state"] == "overlay_enriched_fact"
        assert overlay["usable_for_decision_now"] is False
        assert overlay["not_allowed_as"] == ["proof", "route_seed", "execution_seed", "solve_claim"]


def test_future_probe_manifests_are_disabled() -> None:
    record = stage5eh_data("diagnostic_probe_manifest_records")

    assert record["probe_manifest_count"] == 23
    assert record["all_run_now_false"] is True
    assert all(probe["run_now"] is False for probe in record["records"])
    assert all(probe["execution_enabled"] is False for probe in record["records"])


def test_stage5eh_routes_to_stage5ei_and_guardrails_closed() -> None:
    summary = stage5eh_data("summary")

    assert summary["recommended_next_stage_id"] == "stage-5ei"
    assert summary["target_priority_decision_created_now"] is False
    assert summary["pivot_target_selected_now"] is False
    assert summary["route_extraction_performed_now"] is False
    assert summary["real_byte_stream_generated"] is False
    assert summary["cuda_execution_performed"] is False
    assert summary["solve_claim"] is False


def test_stage5eh_validators_pass() -> None:
    assert stage5eh.validate_stage5eh_number_fact_overlays().ok
    assert stage5eh.validate_stage5eh_current_truth_doc_staleness().ok
    assert stage5eh.validate_stage5eh_sidecar_gates().ok
    assert stage5eh.validate_stage5eh_governance_scope().ok
