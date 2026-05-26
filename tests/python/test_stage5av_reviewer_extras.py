from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5av_reviewer_extra_possible_tokens_are_preserved() -> None:
    payload = yaml.safe_load(
        (
            ROOT / "data/token-block/stage5av-reviewer-extra-possible-tokens.yaml"
        ).read_text(encoding="utf-8")
    )
    assert payload["reviewer_extra_possible_token_count"] == 13
    assert all(record["in_generated_candidate_tokens"] is False for record in payload["records"])
    assert all(record["reviewer_extra_token_status"] == "preserved_for_variant_controls" for record in payload["records"])
