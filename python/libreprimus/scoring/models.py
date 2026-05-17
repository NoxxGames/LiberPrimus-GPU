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
    notes: list[str] = field(default_factory=list)
