from __future__ import annotations

from libreprimus.operator_console.source_browser.entries import SourceBrowserEntry
from libreprimus.operator_console.source_browser.number_facts import (
    number_fact_table_display,
    zero_fact_review_state,
)


def test_zero_facts_default_to_not_reviewed() -> None:
    entry = SourceBrowserEntry(
        entry_id="zero",
        entry_type="source_lock",
        category="Source-locks",
        title="zero",
        summary="zero",
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
        source_record_path="data/historical-route/zero.yaml",
    )

    assert zero_fact_review_state(entry, overlays=[]) == "zero_extracted_facts_not_reviewed"
    assert number_fact_table_display(entry, overlays=[]) == "not reviewed"
