from __future__ import annotations

from libreprimus.operator_console.source_browser.entries import SourceBrowserEntry
from libreprimus.operator_console.source_browser.filters import filter_entries


def _entry(entry_id: str, facts: list[dict[str, object]]) -> SourceBrowserEntry:
    return SourceBrowserEntry(
        entry_id=entry_id,
        entry_type="source_lock",
        category="Source-locks",
        title=entry_id,
        summary=entry_id,
        stage_id="stage-5dt",
        record_type="fixture",
        candidate_family_id=None,
        source_type=None,
        source_status=None,
        trust_tier=None,
        confidence=None,
        selected_now=False,
        solve_claim=False,
        execution_allowed=False,
        source_lock_only=True,
        number_facts=facts,
        source_record_path=f"data/historical-route/{entry_id}.yaml",
    )


def test_reviewability_search_filters() -> None:
    entries = [_entry("zero", []), _entry("vague", [{"claim_id": "x", "value": 1}])]

    assert [entry.entry_id for entry in filter_entries(entries, search="not-reviewed:number-facts")] == ["zero"]
    assert [entry.entry_id for entry in filter_entries(entries, search="needs:fact-enrichment")] == ["vague"]
