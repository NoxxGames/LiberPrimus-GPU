from __future__ import annotations

from libreprimus.operator_console.source_browser.number_facts import load_enrichment_overlays
from libreprimus.token_block.stage5du import OVERLAY_DIR
from test_stage5du_common import ROOT, ensure_stage5du_built, load_yaml


def test_stage5du_overlay_collection_loads_as_individual_overlays() -> None:
    ensure_stage5du_built()
    overlays = load_enrichment_overlays(ROOT / OVERLAY_DIR)
    stage5du_overlays = [overlay for overlay in overlays if overlay["overlay_id"].startswith("stage5du_")]
    assert len(stage5du_overlays) == 6
    assert all(overlay["usable_for_decision_now"] is False for overlay in stage5du_overlays)
    assert all("solve_claim" in overlay["not_allowed_as"] for overlay in stage5du_overlays)


def test_stage5du_number_fact_readiness_does_not_backfill_old_records() -> None:
    ensure_stage5du_built()
    summary = load_yaml("data/project-state/stage5du-number-fact-card-readiness-summary.yaml")
    assert summary["candidate_number_fact_count"] == 6
    assert summary["enrichment_overlay_count"] == 6
    assert summary["stage5du_does_not_backfill_all_old_records"] is True
    assert summary["usable_for_target_priority_now"] is False
