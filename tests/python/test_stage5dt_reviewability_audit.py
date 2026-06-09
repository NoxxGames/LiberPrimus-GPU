from __future__ import annotations

from test_stage5dt_common import ensure_stage5dt_built, load_yaml


def test_reviewability_audit_counts_expected_states() -> None:
    ensure_stage5dt_built()
    audit = load_yaml("data/project-state/stage5dt-number-fact-reviewability-audit.yaml")
    assert audit["audit_created"] is True
    assert audit["total_number_fact_cards_extracted"] >= 1
    assert audit["vague_fact_card_count"] >= 1
    assert audit["entries_with_zero_extracted_number_facts_not_reviewed"] >= 1
    assert audit["examples_vague_facts"]
    assert audit["review_performed_now"] is False
