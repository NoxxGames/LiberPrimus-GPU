from __future__ import annotations

from libreprimus.scoring.minimal_triage import score_text
from libreprimus.scoring.validation import validate_minimal_triage_score


def test_readable_synthetic_candidate_gets_better_label_than_garbage() -> None:
    readable = validate_minimal_triage_score(score_text("THE AND WE CAN"))
    garbage = validate_minimal_triage_score(score_text("QXQXQXQXZZZZ"))

    assert readable["length_normalized_score"] > garbage["length_normalized_score"]
    assert readable["confidence_label"] in {"lead", "weak_lead", "noisy"}
    assert garbage["confidence_label"] == "garbage"
    assert readable["no_solve_claim"] is True


def test_impossible_bigram_penalty_works() -> None:
    score = validate_minimal_triage_score(score_text("QX JZ ZX"))

    assert score["impossible_bigram_count"] >= 3
    assert score["impossible_bigram_penalty"] > 0
    assert any("impossible_bigrams" in feature for feature in score["negative_features"])


def test_repeated_symbol_penalty_works() -> None:
    score = validate_minimal_triage_score(score_text("AAAAABBBBBCCCC"))

    assert score["repeated_character_penalty"] > 0
    assert any("repeated_penalty" in feature for feature in score["negative_features"])


def test_separator_aware_word_count_is_reported() -> None:
    score = validate_minimal_triage_score(score_text("THE AND WE CAN"))

    assert score["separator_aware_word_count"] >= 4
    assert "separator_words=4" in score["positive_features"]
