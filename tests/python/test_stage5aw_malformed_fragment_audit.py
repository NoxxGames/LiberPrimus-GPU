from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5aw_malformed_fragments_are_audited_and_excluded() -> None:
    payload = yaml.safe_load(
        (ROOT / "data/token-block/stage5aw-malformed-possible-token-fragments.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert payload["malformed_possible_token_fragment_count"] == 3
    assert payload["fragments_excluded_from_reviewer_extra_tokens"] is True
    assert all(record["included_in_reviewer_extra_possible_tokens"] is False for record in payload["records"])
    assert any("?4" in record["extracted_tokens"] for record in payload["records"])
    assert any("3?" in record["extracted_tokens"] for record in payload["records"])
