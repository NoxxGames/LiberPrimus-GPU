from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5aw_possible_token_parser_policy_blocks_prose_extras() -> None:
    policy = yaml.safe_load(
        (ROOT / "data/token-block/stage5aw-possible-token-parser-policy.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert policy["possible_tokens_value_stops_at_next_semicolon"] is True
    assert policy["extract_token_prefix_from_prose_segment"] is True
    assert policy["extract_visual_placeholder_from_prose"] is True
    assert policy["prose_fragments_in_reviewer_extra_tokens_allowed"] is False
    assert policy["visual_placeholder_variant_byte_stream_eligible"] is False
