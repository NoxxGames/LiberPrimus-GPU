from __future__ import annotations

from test_stage5ds_common import ROOT, ensure_stage5ds_built


def test_stage5ds_chatgpt_context_contains_handoff() -> None:
    ensure_stage5ds_built()
    text = (ROOT / "ChatGPT-ContextFile.md").read_text(encoding="utf-8")
    assert "Stage 5DS expanded music/Ouroboros/token-block static addendum" in text
    assert "Stage 5DT source-review readiness planning" in text
    assert "right-side/right-dock" in text
    assert "cbe7a7ba61ed7eb75cf99cdef704b7d4" in text
