from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.operator_console.source_browser.entries import SourceBrowserEntry
from libreprimus.operator_console.source_browser.number_facts import (
    load_enrichment_overlays,
    normalize_entry_number_facts,
)


def test_overlay_applies_without_mutating_source_record(tmp_path: Path) -> None:
    root = tmp_path / "overlays"
    root.mkdir()
    overlay = {
        "record_type": "source_browser_number_fact_enrichment_overlay",
        "overlay_id": "nf_overlay_fixture",
        "source_record_path": "data/historical-route/fixture.yaml",
        "source_fact_id": "claim_only",
        "display_label": "Enriched claim",
        "value": 1894,
        "value_type": "rune_count",
        "operation_type": "section_count_equality",
        "why_stored": "Explains the claim for review",
        "verification_status": "canonical_transcript_required",
        "review_state": "overlay_enriched_fact",
        "usable_for_decision_now": False,
        "not_allowed_as": ["proof", "route_seed", "solve_claim"],
    }
    (root / "fixture.yaml").write_text(yaml.safe_dump(overlay), encoding="utf-8")
    original_fact = {"claim_id": "claim_only", "value": 1894}
    entry = SourceBrowserEntry(
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
        number_facts=[original_fact],
        source_record_path="data/historical-route/fixture.yaml",
    )

    cards = normalize_entry_number_facts(entry, overlays=load_enrichment_overlays(root))

    assert cards[0].overlay_applied is True
    assert cards[0].review_state == "overlay_enriched_fact"
    assert original_fact == {"claim_id": "claim_only", "value": 1894}


def test_overlay_templates_are_ignored(tmp_path: Path) -> None:
    template_dir = tmp_path / "overlays" / "templates"
    template_dir.mkdir(parents=True)
    (template_dir / "example-overlay.yaml").write_text("overlay_id: template\n", encoding="utf-8")

    assert load_enrichment_overlays(tmp_path / "overlays") == []
