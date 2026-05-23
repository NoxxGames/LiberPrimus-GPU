from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ai_deep_research_pack_has_sequential_order_and_context_files() -> None:
    payload = yaml.safe_load(Path("data/source-harvester/stage5ai-deep-research-pack-format.yaml").read_text(encoding="utf-8"))
    assert payload["deep_research_pack_records"] == 10
    assert payload["sequential_order_present"] is True
    assert payload["do_not_assume_files_present"] is True
    assert payload["known_questions_files_present"] is True
    assert payload["private_deep_research_allowed"] is True
