from __future__ import annotations

from libreprimus.operator_console.source_browser.entries import SourceBrowserEntry
from libreprimus.operator_console.source_browser.number_facts import normalize_entry_number_facts


def _entry(facts: list[dict[str, object]]) -> SourceBrowserEntry:
    return SourceBrowserEntry(
        entry_id="fixture",
        entry_type="source_lock",
        category="Number facts",
        title="fixture",
        summary="fixture",
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
        source_record_path="data/historical-route/fixture.yaml",
    )


def test_rich_fact_card_normalizes_as_rich() -> None:
    cards = normalize_entry_number_facts(
        _entry(
            [
                {
                    "fact_id": "rich",
                    "display_label": "Rich fact",
                    "value": 2472,
                    "value_type": "gp_sum",
                    "operation_type": "gp_sum",
                    "relation": "A declared relation",
                    "why_stored": "For reviewability",
                }
            ]
        ),
        overlays=[],
    )
    assert cards[0].review_state == "rich_fact_card"
    assert cards[0].usable_for_decision_now is False


def test_claim_id_value_only_is_vague() -> None:
    cards = normalize_entry_number_facts(
        _entry([{"claim_id": "claim_only", "value": 1894}]),
        overlays=[],
    )
    assert cards[0].review_state == "vague_fact_enrichment_needed"
    assert cards[0].needs_enrichment is True
