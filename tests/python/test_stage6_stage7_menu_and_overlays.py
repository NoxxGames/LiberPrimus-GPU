from __future__ import annotations

from test_stage6_common import stage6_data


def test_stage6_routes_to_stage6b_by_default() -> None:
    summary = stage6_data("summary")
    assert summary["recommended_next_stage_id"] == "stage-6b"
    assert "Final finite Stage 7 probe manifest" in summary["recommended_next_stage_title"]


def test_stage6_stage7_menu_is_future_only() -> None:
    payload = stage6_data("stage7_candidate_menu")
    assert payload["stage6b_finalization_required"] is True
    assert payload["candidate_menu_status"] == "partial_foundation_only"
    assert payload["not_stage7_execution_manifest"] is True
    assert payload["stage6c_final_menu_required"] is True
    assert payload["stage7_execution_allowed_from_this_menu"] is False
    assert payload["stage7_zip_archive_creation_allowed_from_this_menu"] is False
    assert payload["candidate_count"] == 11
    for candidate in payload["stage7_candidates"]:
        assert candidate["stage6_run_now"] is False
        assert candidate["execution_enabled_now"] is False
        assert candidate["result_bundle_policy_required"] is True
        assert candidate["readiness_class"].startswith("stage7_")


def test_stage6_optional_source_browser_overlays_are_review_only() -> None:
    payload = stage6_data("observation_rune_frequency_overlays")
    assert payload["number_fact_review_batch_stage"] is False
    assert payload["usable_for_decision_now"] is False
    for overlay in payload["overlays"]:
        assert overlay["usable_for_decision_now"] is False
        assert overlay["not_allowed_as"] == ["proof", "route_seed", "execution_seed", "solve_claim"]
