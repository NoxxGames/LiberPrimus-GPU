from __future__ import annotations

from test_stage5dv_common import ROOT, ensure_stage5dv_built, load_yaml


def test_stage5dv_chatgpt_context_has_required_sections() -> None:
    ensure_stage5dv_built()
    text = (ROOT / "ChatGPT-ContextFile.md").read_text(encoding="utf-8")
    required = [
        "## Current Project State",
        "## Stage 5DV Source Browser Repair",
        "## Source Browser Path Rules",
        "## Stage 5DU Six-Thread Summary",
        "## Top Candidate Stack",
        "## Number-Fact Review Principle",
        "## Guardrails",
        "Stage 5DW",
    ]
    for phrase in required:
        assert phrase in text
    assert "BEGIN RAW SOURCE" not in text


def test_stage5dv_chatgpt_context_summary_records_no_raw_body() -> None:
    ensure_stage5dv_built()
    summary = load_yaml("data/project-state/stage5dv-chatgpt-context-hardening-summary.yaml")
    assert summary["chatgpt_context_updated"] is True
    assert summary["stage5du_six_thread_summary_present"] is True
    assert summary["source_browser_path_rules_present"] is True
    assert summary["current_next_stage_shift_to_stage5dw_present"] is True
    assert summary["raw_source_body_included"] is False
