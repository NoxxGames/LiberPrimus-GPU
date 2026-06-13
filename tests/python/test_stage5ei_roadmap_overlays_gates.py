from __future__ import annotations

from libreprimus.token_block import stage5ei
from test_stage5ei_common import stage5ei_data


def test_stage5ei_stage6_7_8_9_roadmap_boundaries() -> None:
    payload = stage5ei_data("stage6_7_8_9_roadmap")
    roadmap = payload["stage_roadmap"]

    assert roadmap["stage6_plan"]["execution_allowed"] is False
    assert roadmap["stage7_plan"]["execution_allowed"] == "bounded_diagnostics_only_after_stage6"
    assert roadmap["stage8_plan"]["execution_allowed"] is False
    assert roadmap["stage9_plan"]["execution_allowed"] == "bounded_experiments_only_after_stage8"


def test_stage5ei_overlays_are_review_only_and_meaningful() -> None:
    payload = stage5ei_data("overlay_collection")
    topics = {overlay["overlay_topic"] for overlay in payload["number_fact_overlays"]}

    assert payload["overlay_count"] == 7
    for topic, _label in stage5ei.OVERLAY_TOPICS:
        assert topic in topics
    for overlay in payload["number_fact_overlays"]:
        assert overlay["review_state"] == "overlay_enriched_fact"
        assert overlay["usable_for_decision_now"] is False
        assert overlay["not_allowed_as"] == ["proof", "route_seed", "execution_seed", "solve_claim"]


def test_stage5ei_guardrails_are_closed() -> None:
    for key in stage5ei.DATA_PATHS:
        payload = stage5ei_data(key)
        for field, expected in stage5ei.FALSE_GUARDRAILS.items():
            assert payload[field] is expected, (key, field)
        assert payload["selected_next_solve_target_id"] is None

