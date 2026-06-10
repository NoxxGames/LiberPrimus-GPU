from __future__ import annotations

from libreprimus.operator_console.source_browser.entries import SourceBrowserEntry
from libreprimus.operator_console.source_browser.number_facts import (
    normalize_entry_number_facts,
    number_fact_table_display,
)
from test_stage5dx_common import ensure_stage5dx_built, load_yaml


def _entry(number_facts: list[dict[str, object]] | None = None) -> SourceBrowserEntry:
    return SourceBrowserEntry(
        entry_id="stage5dx-test-entry",
        entry_type="source_lock",
        category="Number facts",
        title="Stage 5DX test entry",
        summary="test",
        stage_id="stage-5dx",
        record_type="stage5dx_test",
        candidate_family_id=None,
        source_type=None,
        source_status=None,
        trust_tier=None,
        confidence=None,
        selected_now=False,
        solve_claim=False,
        execution_allowed=False,
        source_lock_only=False,
        source_record_path="data/historical-route/stage5dx-test-entry.yaml",
        number_facts=number_facts or [],
    )


def test_stage5dx_overlay_only_fact_cards_render_for_zero_extracted_fact_entry() -> None:
    entry = _entry()
    overlay = {
        "record_type": "source_browser_number_fact_enrichment_overlay",
        "overlay_id": "stage5dx_overlay_only_test",
        "source_record_path": entry.source_record_path,
        "source_fact_id": "overlay_only_fact",
        "display_label": "Overlay-only fact = 56311",
        "short_label": "Overlay-only = 56311",
        "value": 56311,
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
    assert number_fact_table_display(entry, [overlay]) == "Overlay-only = 56311"


def test_stage5dx_overlay_collection_requires_overlay_only_cards() -> None:
    ensure_stage5dx_built()
    summary = load_yaml("data/project-state/stage5dx-summary.yaml")

    assert summary["overlay_only_fact_cards_supported"] is True
    assert summary["overlay_only_fact_cards_validated"] is True
    assert summary["overlay_only_cards_required_count"] == 23
