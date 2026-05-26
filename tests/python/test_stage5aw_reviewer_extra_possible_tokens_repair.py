from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5aw_reviewer_extra_possible_tokens_are_valid_two_char_options() -> None:
    payload = yaml.safe_load(
        (
            ROOT / "data/token-block/stage5aw-repaired-reviewer-extra-possible-tokens.yaml"
        ).read_text(encoding="utf-8")
    )
    extras = [record["reviewer_extra_possible_token"] for record in payload["records"]]
    assert payload["repaired_reviewer_extra_possible_token_count"] == 10
    assert {"1i", "0j", "Oj", "1I"}.issubset(set(extras))
    assert all(len(token) == 2 and not any(char.isspace() for char in token) for token in extras)
    assert "O4 row overlay supports ?4" not in extras
    assert "3l row overlay supports 3? but suffix remains ambiguous" not in extras
