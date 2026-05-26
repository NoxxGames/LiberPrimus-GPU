from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5aw_visual_placeholders_are_preserved_separately() -> None:
    payload = yaml.safe_load(
        (
            ROOT / "data/token-block/stage5aw-repaired-unresolved-token-variant-records.yaml"
        ).read_text(encoding="utf-8")
    )
    records = {record["challenge_id"]: record for record in payload["records"]}
    case013 = records["stage5at-token-case-013"]
    assert case013["possible_tokens"] == ["04", "O4", "?4"]
    placeholder = next(
        item for item in case013["possible_token_details"] if item["token"] == "?4"
    )
    assert placeholder["possible_token_source"] == "visual_placeholder_from_reviewer_notes"
    assert placeholder["primary60_status"] == "visual_placeholder_unmappable"
    assert placeholder["primary60_mappable"] is False
    assert placeholder["variant_byte_stream_eligible"] is False
