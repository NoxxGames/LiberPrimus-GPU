from __future__ import annotations

from pathlib import Path

from test_stage5dz_common import ensure_stage5dz_built


def test_stage5dz_chatgpt_context_mentions_triangle_page32_and_guardrails() -> None:
    ensure_stage5dz_built()

    text = Path("ChatGPT-ContextFile.md").read_text(encoding="utf-8")

    assert "Stage 5DZ - Triangle/Page32 bounded-solve findings source-lock" in text
    assert "No validated plaintext found." in text
    assert "56311 from center word 41/WYNN reaches word52" in text
    assert "Red header gives 463 -> prime(463)=3299 and progressive sum 2472." in text
    assert "3299->3298->3296->3294->3288->3278->3258->3222->3152->3038->2838->2472" in text
    assert "No target selected." in text
