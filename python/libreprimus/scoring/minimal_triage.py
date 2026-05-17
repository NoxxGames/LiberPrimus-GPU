"""Minimal deterministic scoring for bounded CPU candidate triage."""

from __future__ import annotations

from collections import Counter
import math
import re

from libreprimus.scoring.models import MinimalTriageScore
from libreprimus.scoring.word_lists import load_tiny_common_words

VOWELS = set("AEIOUY")
WORD_RE = re.compile(r"[A-Z]+")


def score_text(text: str, *, common_words: list[str] | None = None) -> MinimalTriageScore:
    words = common_words if common_words is not None else load_tiny_common_words()
    upper = text.upper()
    letters = [char for char in upper if "A" <= char <= "Z"]
    unknown_symbol_count = sum(1 for char in text if not (char.isprintable() and (char.isalnum() or char.isspace())))
    printable_ratio = _ratio(sum(1 for char in text if char.isprintable()), len(text))
    vowel_ratio = _ratio(sum(1 for char in letters if char in VOWELS), len(letters))
    common_hits = _common_word_hits(upper, words)
    repeated_penalty = _repeated_character_penalty(upper)
    entropy = _entropy(letters)
    total = (
        len(letters) * 0.01
        + len(common_hits) * 3.0
        + vowel_ratio * 5.0
        + printable_ratio * 2.0
        + entropy
        - unknown_symbol_count * 2.0
        - repeated_penalty
    )
    return MinimalTriageScore(
        record_type="minimal_triage_score",
        score_schema="minimal-triage-score-v0",
        total_score=round(total, 6),
        latin_letter_count=len(letters),
        unknown_symbol_count=unknown_symbol_count,
        vowel_ratio=round(vowel_ratio, 6),
        common_word_hit_count=len(common_hits),
        common_word_hits=common_hits,
        repeated_character_penalty=round(repeated_penalty, 6),
        printable_ratio=round(printable_ratio, 6),
        entropy=round(entropy, 6),
        notes=["Minimal triage only; not solve evidence."],
    )


def _ratio(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def _common_word_hits(text: str, words: list[str]) -> list[str]:
    collapsed = "".join(WORD_RE.findall(text))
    hits = [word for word in words if word in collapsed]
    return sorted(set(hits))


def _repeated_character_penalty(text: str) -> float:
    penalty = 0.0
    run_char = ""
    run_length = 0
    for char in text:
        if char == run_char and char.isalpha():
            run_length += 1
            if run_length >= 4:
                penalty += 0.25
        else:
            run_char = char
            run_length = 1
    return penalty


def _entropy(letters: list[str]) -> float:
    if not letters:
        return 0.0
    counts = Counter(letters)
    total = len(letters)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())
