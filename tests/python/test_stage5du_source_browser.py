from __future__ import annotations

from test_stage5du_common import ensure_stage5du_built, load_yaml


def test_stage5du_source_browser_loadability_summary_has_no_errors() -> None:
    ensure_stage5du_built()
    summary = load_yaml("data/project-state/stage5du-source-browser-loadability-summary.yaml")
    assert summary["source_browser_records_scanned"] == 1489
    assert summary["source_browser_entries_loaded"] == 1490
    assert summary["stage5du_entries_loaded"] == 103
    assert summary["source_browser_validation_error_count"] == 0
    assert summary["source_browser_fact_cards_extracted"] == 26


def test_stage5du_chatgpt_context_points_to_stage5dv() -> None:
    ensure_stage5du_built()
    context = load_yaml("data/project-state/stage5du-chatgpt-context-update-summary.yaml")
    assert context["chatgpt_context_updated"] is True
    assert context["stage5du_section_present"] is True
    assert context["raw_source_body_included"] is False
