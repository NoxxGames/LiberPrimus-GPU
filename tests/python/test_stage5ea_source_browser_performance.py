from __future__ import annotations

from libreprimus.operator_console.source_browser.entries import SourceBrowserEntry
from libreprimus.operator_console.source_browser.filters import searchable_text
from libreprimus.operator_console.source_browser.number_facts import (
    NumberFactOverlayCache,
    normalize_entry_number_facts,
    number_fact_table_display,
)
from test_stage5ea_common import ensure_stage5ea_built, load_yaml


def _entry() -> SourceBrowserEntry:
    return SourceBrowserEntry(
        entry_id="stage5ea-test-entry",
        entry_type="test",
        category="Number facts",
        title="Test",
        summary="Test entry",
        stage_id="stage-5ea",
        record_type="stage5ea_test_record",
        candidate_family_id=None,
        source_type=None,
        source_status=None,
        trust_tier=None,
        confidence=None,
        selected_now=False,
        solve_claim=False,
        execution_allowed=False,
        source_lock_only=False,
        source_record_path="data/test/stage5ea-source.yaml",
        number_facts=[
            {
                "source_fact_id": "fact-1",
                "value": 153,
                "display_label": "GP sum 153",
                "short_label": "153",
                "value_type": "gp_sum",
                "operation_type": "gp_sum",
                "why_stored": "synthetic Stage 5EA cache test fixture",
                "relation": "synthetic equality",
            }
        ],
    )


def test_number_fact_overlay_cache_reused_by_display_and_search() -> None:
    ensure_stage5ea_built()
    cache = NumberFactOverlayCache.from_overlays([])
    entry = _entry()

    assert cache.load_count == 0
    assert number_fact_table_display(entry, overlay_cache=cache) == "153"
    assert "gp sum 153" in searchable_text(entry, overlay_cache=cache)
    assert normalize_entry_number_facts(entry, overlay_cache=cache)[0].value == 153


def test_source_browser_performance_record_names_overlay_cache() -> None:
    ensure_stage5ea_built()

    record = load_yaml("data/project-state/stage5ea-source-browser-fact-card-performance.yaml")

    assert record["overlay_cache_implemented"] is True
    assert record["overlay_index_loaded_once_per_refresh"] is True
    assert record["table_filter_detail_reuse_overlay_cache"] is True
