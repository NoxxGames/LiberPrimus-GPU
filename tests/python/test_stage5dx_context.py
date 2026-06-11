from __future__ import annotations

from test_stage5dx_common import ROOT, ensure_stage5dx_built, load_yaml


def test_stage5dx_chatgpt_context_contains_durable_summary() -> None:
    ensure_stage5dx_built()
    context = (ROOT / "ChatGPT-ContextFile.md").read_text(encoding="utf-8")
    summary = load_yaml("data/project-state/stage5dx-chatgpt-context-update-summary.yaml")

    assert "## Stage 5DX - Number-fact review batch 002" in context
    assert "Stage 5DX enriched 20 selected visual/red-heading/transform source-lock entries" in context
    assert "Stage 5EC should continue with number-fact review batch 003" in context
    assert summary["chatgpt_context_updated"] is True
    assert summary["raw_source_body_included"] is False
