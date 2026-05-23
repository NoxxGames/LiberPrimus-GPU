from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ai_missing_source_plan_includes_priority_gaps() -> None:
    payload = yaml.safe_load(Path("data/source-harvester/stage5ai-missing-source-plan.yaml").read_text(encoding="utf-8"))
    assert payload["missing_source_records"] == 20
    assert payload["missing_a1_a2_count"] >= 1
    source_ids = {record["source_id"] for record in payload["records"]}
    assert "pastebin_vgmk330j_lp_runes_prime_values" in source_ids
    assert "solved_page_google_sheet" in source_ids
    assert "chapterized_rune_map_google_doc" in source_ids
