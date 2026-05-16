"""Models for Stage 0C legacy Pastebin ingestion."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

SOURCE_ID = "pastebin-vGMK330j"
SOURCE_LOCAL_FILENAME = "58-Pages-In-Runes-With-Prime-Values-Pastebin.txt"


def to_jsonable(value: Any) -> Any:
    """Convert dataclasses and paths into deterministic JSON-friendly values."""
    if hasattr(value, "__dataclass_fields__"):
        return {key: to_jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]
    return value


@dataclass(frozen=True)
class LegacyPastebinWarning:
    record_type: str
    source_id: str
    source_sha256: str
    source_local_filename: str
    message: str
    pair_index: int | None = None
    source_line_number: int | None = None
    word_index: int | None = None
    glyph_index: int | None = None


@dataclass(frozen=True)
class LegacyPastebinLinePair:
    record_type: str
    source_id: str
    source_sha256: str
    source_local_filename: str
    pair_index: int
    source_rune_line_number: int
    source_prime_line_number: int | None
    raw_rune_line: str
    raw_prime_line: str | None
    rune_words: list[str]
    prime_words: list[list[int]]
    decimal_index_words: list[list[int | None]]
    word_count_match: bool
    per_word_length_match: bool
    validated_prime_mapping: bool
    validation_status: str
    page_index_inferred: int | None
    page_boundary_confidence: str
    trusted_as_canonical: bool
    warnings: list[str] = field(default_factory=list)
    empty_pair: bool = False
    glyph_alias_inferred: bool = False


@dataclass(frozen=True)
class LegacyPastebinAnchor:
    record_type: str
    source_id: str
    anchor_type: str
    page_label_candidate: str
    confidence: str
    canonical_page_boundary: bool
    pair_index: int
    evidence: str


@dataclass(frozen=True)
class LegacyPastebinSummary:
    record_type: str
    source_id: str
    source_sha256: str
    source_local_filename: str
    line_pair_count: int
    rune_row_count: int
    prime_value_row_count: int
    empty_pair_count: int
    validation_warning_count: int
    unknown_glyph_count: int
    unknown_prime_value_count: int
    all_records_trusted_as_canonical: bool
    canonical_corpus_allowed: bool
    page_boundary_status: str


@dataclass(frozen=True)
class LegacyPastebinExtraction:
    line_pairs: list[LegacyPastebinLinePair]
    anchors: list[LegacyPastebinAnchor]
    warnings: list[LegacyPastebinWarning]
    summary: LegacyPastebinSummary
