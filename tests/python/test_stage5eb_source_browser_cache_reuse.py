from __future__ import annotations

from libreprimus.operator_console.source_browser.entries import SourceBrowserEntry
from libreprimus.operator_console.source_browser.filters import searchable_text
from libreprimus.operator_console.source_browser.number_facts import (
    NumberFactOverlayCache,
    normalize_entry_number_facts,
    number_fact_table_display,
    reviewability_counts,
)
from test_stage5eb_common import ensure_stage5eb_built, load_yaml


def _entry() -> SourceBrowserEntry:
    return SourceBrowserEntry(
        entry_id="stage5eb-test-entry",
        entry_type="test",
        category="Number facts",
        title="Test",
        summary="Test entry",
        stage_id="stage-5eb",
        record_type="stage5eb_test_record",
        candidate_family_id=None,
        source_type=None,
        source_status=None,
        trust_tier=None,
        confidence=None,
        selected_now=False,
        solve_claim=False,
        execution_allowed=False,
        source_lock_only=False,
        source_record_path="data/test/stage5eb-source.yaml",
        number_facts=[
            {
                "source_fact_id": "fact-1",
                "value": 153,
                "display_label": "GP sum 153",
                "short_label": "153",
                "value_type": "gp_sum",
                "operation_type": "gp_sum",
                "why_stored": "synthetic Stage 5EB cache test fixture",
                "relation": "synthetic equality",
            }
        ],
    )


def test_stage5eb_source_browser_reuses_overlay_cache_callers() -> None:
    ensure_stage5eb_built()
    cache = NumberFactOverlayCache.from_overlays([])
    entry = _entry()

    assert cache.load_count == 0
    assert number_fact_table_display(entry, overlay_cache=cache) == "153"
    assert "gp sum 153" in searchable_text(entry, overlay_cache=cache)
    assert normalize_entry_number_facts(entry, overlay_cache=cache)[0].value == 153
    assert reviewability_counts([entry], overlay_cache=cache)["entries_with_extracted_number_facts"] == 1


def test_stage5eb_source_browser_cache_reuse_record() -> None:
    ensure_stage5eb_built()

    record = load_yaml("data/project-state/stage5eb-source-browser-cache-reuse-evidence.yaml")

    assert record["source_browser_overlay_cache_constructed_once_per_index_load"] is True
    assert record["source_browser_table_display_uses_shared_overlay_cache"] is True
    assert record["source_browser_filtering_uses_shared_overlay_cache"] is True
    assert record["source_browser_detail_panel_uses_shared_overlay_cache"] is True
    assert record["source_browser_reviewability_counts_use_single_overlay_cache"] is True
    assert record["no_per_row_overlay_file_scan"] is True
