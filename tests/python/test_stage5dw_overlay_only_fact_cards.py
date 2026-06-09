from __future__ import annotations

from libreprimus.operator_console.source_browser.entries import SourceBrowserEntry
from libreprimus.operator_console.source_browser.number_facts import (
    normalize_entry_number_facts,
    number_fact_table_display,
)
from test_stage5dw_common import ensure_stage5dw_built, load_yaml


def _entry(number_facts: list[dict[str, object]] | None = None) -> SourceBrowserEntry:
    return SourceBrowserEntry(
        entry_id="stage5dw-test-entry",
        entry_type="source_lock",
        category="Number facts",
        title="Stage 5DW test entry",
        summary="test",
        stage_id="stage-5dw",
        record_type="stage5dw_test",
        candidate_family_id=None,
        source_type=None,
        source_status=None,
        trust_tier=None,
        confidence=None,
        selected_now=False,
        solve_claim=False,
        execution_allowed=False,
        source_lock_only=False,
        source_record_path="data/historical-route/stage5dw-test-entry.yaml",
        number_facts=number_facts or [],
    )


def test_overlay_only_fact_cards_render_for_zero_extracted_fact_entry() -> None:
    entry = _entry()
    overlay = {
        "record_type": "source_browser_number_fact_enrichment_overlay",
        "overlay_id": "stage5dw_overlay_only_test",
        "source_record_path": entry.source_record_path,
        "source_fact_id": "overlay_only_fact",
        "display_label": "Overlay-only fact = 20",
        "short_label": "Overlay-only = 20",
        "value": 20,
        "value_type": "sum",
        "operation_type": "sum",
        "verification_status": "arithmetic_verified_metadata_only",
        "review_state": "overlay_enriched_fact",
        "usable_for_decision_now": False,
        "not_allowed_as": ["proof", "route_seed", "execution_seed", "solve_claim"],
    }

    cards = normalize_entry_number_facts(entry, [overlay])

    assert len(cards) == 1
    assert cards[0].source_fact_id == "overlay_only_fact"
    assert cards[0].overlay_applied is True
    assert number_fact_table_display(entry, [overlay]) == "Overlay-only = 20"


def test_overlay_enrichment_still_updates_existing_raw_fact() -> None:
    entry = _entry([{"source_fact_id": "raw_fact", "value": 1}])
    overlay = {
        "record_type": "source_browser_number_fact_enrichment_overlay",
        "overlay_id": "stage5dw_existing_fact_overlay",
        "source_record_path": entry.source_record_path,
        "source_fact_id": "raw_fact",
        "display_label": "Raw fact enriched = 2",
        "short_label": "Raw fact enriched",
        "value": 2,
        "value_type": "sum",
        "operation_type": "sum",
        "verification_status": "arithmetic_verified_metadata_only",
        "review_state": "overlay_enriched_fact",
        "usable_for_decision_now": False,
        "not_allowed_as": ["proof", "route_seed", "execution_seed", "solve_claim"],
    }

    cards = normalize_entry_number_facts(entry, [overlay])

    assert len(cards) == 1
    assert cards[0].short_label == "Raw fact enriched"
    assert cards[0].value == 2


def test_zero_fact_not_reviewed_changes_only_with_overlay() -> None:
    entry = _entry()
    assert number_fact_table_display(entry, []) == "not reviewed"


def test_stage5dw_overlay_collection_has_overlay_only_cards() -> None:
    ensure_stage5dw_built()
    collection = load_yaml(
        "data/operator-console/source-browser/number-fact-overlays/"
        "stage5dw-review-batch-001-high-signal-overlays.yaml"
    )
    selected_paths = set(collection["selected_source_record_paths"])
    overlay_paths = {overlay["source_record_path"] for overlay in collection["overlays"]}

    assert collection["overlay_count"] == 37
    assert selected_paths <= overlay_paths
