"""Minimal deterministic scoring for bounded CPU candidate triage."""

from __future__ import annotations

from collections import Counter
import math
import re

from libreprimus.scoring.models import MinimalTriageScore
from libreprimus.scoring.word_lists import load_tiny_common_words, load_tiny_impossible_bigrams

VOWELS = set("AEIOUY")
WORD_RE = re.compile(r"[A-Z]+")
SEGMENT_RE = re.compile(r"[A-Z]{2,}")


def score_text(
    text: str,
    *,
    common_words: list[str] | None = None,
    impossible_bigrams: list[str] | None = None,
) -> MinimalTriageScore:
    words = common_words if common_words is not None else load_tiny_common_words()
    bigrams = impossible_bigrams if impossible_bigrams is not None else load_tiny_impossible_bigrams()
    upper = text.upper()
    letters = [char for char in upper if "A" <= char <= "Z"]
    segments = SEGMENT_RE.findall(upper)
    separator_aware_word_count = _separator_aware_word_count(segments, words)
    unknown_symbol_count = sum(1 for char in text if not (char.isprintable() and (char.isalnum() or char.isspace())))
    printable_ratio = _ratio(sum(1 for char in text if char.isprintable()), len(text))
    vowel_ratio = _ratio(sum(1 for char in letters if char in VOWELS), len(letters))
    common_hits = _common_word_hits(upper, words, segments)
    repeated_penalty = _repeated_character_penalty(upper)
    impossible_hits = _impossible_bigram_hits(upper, bigrams)
    impossible_penalty = len(impossible_hits) * 1.5
    entropy = _entropy(letters)
    vowel_band_score = _vowel_band_score(vowel_ratio)
    no_separator_penalty = 5.0 if len(segments) <= 1 and len(letters) > 24 else 0.0
    length_normalizer = max(1.0, len(letters) / 80.0)
    total = (
        len(letters) * 0.01
        + separator_aware_word_count * 3.0
        + len(common_hits) * 0.65
        + vowel_band_score * 4.0
        + printable_ratio * 2.0
        + entropy
        - unknown_symbol_count * 2.0
        - repeated_penalty
        - impossible_penalty
        - no_separator_penalty
    )
    length_normalized_score = total / length_normalizer
    positive_features = _positive_features(common_hits, separator_aware_word_count, vowel_band_score, printable_ratio)
    negative_features = _negative_features(
        unknown_symbol_count,
        repeated_penalty,
        impossible_hits,
        no_separator_penalty,
        vowel_band_score,
    )
    confidence_label = _confidence_label(length_normalized_score, positive_features, negative_features)
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
        length_normalized_score=round(length_normalized_score, 6),
        separator_aware_word_count=separator_aware_word_count,
        vowel_band_score=round(vowel_band_score, 6),
        impossible_bigram_count=len(impossible_hits),
        impossible_bigram_hits=impossible_hits,
        impossible_bigram_penalty=round(impossible_penalty, 6),
        positive_features=positive_features,
        negative_features=negative_features,
        confidence_label=confidence_label,
        no_solve_claim=True,
        notes=["Minimal triage only; not solve evidence."],
    )


def _ratio(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def _common_word_hits(text: str, words: list[str], segments: list[str]) -> list[str]:
    collapsed = "".join(WORD_RE.findall(text))
    exact = {segment for segment in segments if segment in set(words)}
    embedded = {word for word in words if len(word) >= 3 and word in collapsed}
    hits = sorted(exact | embedded)
    return hits


def _separator_aware_word_count(segments: list[str], words: list[str]) -> int:
    word_set = set(words)
    return sum(1 for segment in segments if segment in word_set)


def _impossible_bigram_hits(text: str, bigrams: list[str]) -> list[str]:
    collapsed = "".join(WORD_RE.findall(text))
    hits = [bigram for bigram in bigrams if bigram in collapsed]
    return sorted(set(hits))


def _vowel_band_score(vowel_ratio: float) -> float:
    if 0.30 <= vowel_ratio <= 0.48:
        return 1.0
    if 0.24 <= vowel_ratio < 0.30 or 0.48 < vowel_ratio <= 0.56:
        return 0.45
    return 0.0


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


def _positive_features(
    common_hits: list[str],
    separator_aware_word_count: int,
    vowel_band_score: float,
    printable_ratio: float,
) -> list[str]:
    features: list[str] = []
    if separator_aware_word_count:
        features.append(f"separator_words={separator_aware_word_count}")
    if common_hits:
        features.append(f"common_hits={len(common_hits)}")
    if vowel_band_score >= 1.0:
        features.append("vowel_ratio_in_target_band")
    if printable_ratio >= 0.98:
        features.append("printable")
    return features


def _negative_features(
    unknown_symbol_count: int,
    repeated_penalty: float,
    impossible_hits: list[str],
    no_separator_penalty: float,
    vowel_band_score: float,
) -> list[str]:
    features: list[str] = []
    if unknown_symbol_count:
        features.append(f"unknown_symbols={unknown_symbol_count}")
    if repeated_penalty:
        features.append(f"repeated_penalty={round(repeated_penalty, 3)}")
    if impossible_hits:
        features.append(f"impossible_bigrams={','.join(impossible_hits)}")
    if no_separator_penalty:
        features.append("no_separator_context")
    if vowel_band_score == 0:
        features.append("vowel_ratio_outside_sanity_band")
    return features


def _confidence_label(score: float, positive_features: list[str], negative_features: list[str]) -> str:
    if score >= 18 and len(positive_features) >= 3 and not negative_features:
        return "lead"
    if score >= 12 and len(positive_features) >= 2 and len(negative_features) <= 1:
        return "weak_lead"
    if score >= 6 and len(negative_features) <= 2:
        return "noisy"
    return "garbage"
