from __future__ import annotations

from pathlib import Path

from test_stage5dy_common import ensure_stage5dy_built, load_yaml


def test_chatgpt_context_contains_validation_policy() -> None:
    ensure_stage5dy_built()
    text = Path("ChatGPT-ContextFile.md").read_text(encoding="utf-8")
    summary = load_yaml("data/project-state/stage5dy-chatgpt-context-update-summary.yaml")

    assert "## Stage 5DY Validation Policy" in text
    assert "PowerShell wildcard expansion differs from Bash" in text
    assert "Stage 5EB remains the next fact-review batch" in text
    assert summary["stage5dy_validation_policy_section_added"] is True
