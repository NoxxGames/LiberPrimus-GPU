from __future__ import annotations

from libreprimus.operator_console.source_browser.entries import SourceBrowserEntry
from libreprimus.operator_console.source_browser.table_model import SourceBrowserTableModel


def _entry(facts: list[dict[str, object]]) -> SourceBrowserEntry:
    return SourceBrowserEntry(
        entry_id="entry",
        entry_type="source_lock",
        category="Number facts",
        title="entry",
        summary="entry",
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
        source_record_path="data/historical-route/entry.yaml",
    )


def test_number_fact_table_display_uses_reviewability_labels() -> None:
    model = SourceBrowserTableModel([_entry([]), _entry([{"claim_id": "x", "value": 1}])], [{"key": "number_facts"}])

    assert model._display(model.entries[0], "number_facts") == "not reviewed"
    assert model._display(model.entries[1], "number_facts") == "1 facts / needs context"
