"""Models for minimal bounded-candidate triage scoring."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class MinimalTriageScore:
    record_type: str
    score_schema: str
    total_score: float
    latin_letter_count: int
    unknown_symbol_count: int
    vowel_ratio: float
    common_word_hit_count: int
    common_word_hits: list[str]
    repeated_character_penalty: float
    printable_ratio: float
    entropy: float
    length_normalized_score: float
    separator_aware_word_count: int
    vowel_band_score: float
    impossible_bigram_count: int
    impossible_bigram_hits: list[str]
    impossible_bigram_penalty: float
    positive_features: list[str]
    negative_features: list[str]
    confidence_label: str
    no_solve_claim: bool
    notes: list[str] = field(default_factory=list)
