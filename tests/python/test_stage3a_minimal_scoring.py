from __future__ import annotations

from libreprimus.scoring.minimal_triage import score_text
from libreprimus.scoring.validation import validate_minimal_triage_score
from libreprimus.scoring.word_lists import load_tiny_common_words


def test_minimal_triage_scoring_is_deterministic() -> None:
    first = validate_minimal_triage_score(score_text("THEANDOFTOIN"))
    second = validate_minimal_triage_score(score_text("THEANDOFTOIN"))

    assert first == second
    assert first["record_type"] == "minimal_triage_score"
    assert first["score_schema"] == "minimal-triage-score-v0"


def test_tiny_word_hits_are_deterministic() -> None:
    words = load_tiny_common_words()
    score = validate_minimal_triage_score(score_text("THEANDWILL", common_words=words))

    assert score["common_word_hit_count"] >= 3
    assert {"THE", "AND", "WILL"}.issubset(set(score["common_word_hits"]))
