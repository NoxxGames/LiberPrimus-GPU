"""Models for Stage 0D Pastebin-to-transcript alignment."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class LineSignature:
    signature_kind: str
    source_index: int
    raw_rune_sequence: str
    normalized_rune_sequence: str
    decimal_index_sequence: list[int]
    word_length_sequence: list[int]
    rune_count: int
    empty_pair: bool
    signature_sha256: str


@dataclass(frozen=True)
class AlignmentCandidate:
    transcript_physical_line_number: int
    match_pass: str
    confidence: str
    confidence_score: float
    variant_mapping_applied: bool = False
    neighborhood_supported: bool = False


@dataclass(frozen=True)
class PastebinTranscriptAlignment:
    record_type: str
    source_id: str
    pastebin_source_sha256: str
    transcript_source_id: str
    transcript_source_sha256: str
    pastebin_pair_index: int
    pastebin_rune_line_number: int
    pastebin_prime_line_number: int | None
    pastebin_rune_count: int
    transcript_candidate_count: int
    best_match: AlignmentCandidate | None
    all_candidates: list[AlignmentCandidate]
    trusted_as_canonical: bool
    canonical_page_boundary: bool
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class GlyphVariantObservation:
    record_type: str
    source_id: str
    source_sha256: str
    observed_glyph: str
    observed_prime_value: int
    inferred_decimal_index: int
    inferred_canonical_glyph_candidate: str
    inferred_latin_label: str
    occurrence_count: int
    matched_transcript_glyphs: list[str]
    variant_policy: str
    trusted_as_canonical: bool
    warnings: list[str]


@dataclass(frozen=True)
class PageBoundaryCandidate:
    record_type: str
    source_id: str
    pastebin_source_sha256: str
    transcript_source_id: str
    transcript_source_sha256: str
    candidate_local_page_index: int | None
    candidate_page_label: str | None
    start_pair_index: int | None
    end_pair_index: int | None
    start_transcript_line: int | None
    end_transcript_line: int | None
    confidence: str
    canonical_page_boundary: bool
    evidence: list[str]
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Stage0DAlignmentSummary:
    record_type: str
    pastebin_source_id: str
    pastebin_source_sha256: str
    transcript_source_id: str
    transcript_source_sha256: str
    transcript_physical_line_count: int
    pastebin_line_pair_count: int
    alignment_record_count: int
    exact_confidence_match_count: int
    high_confidence_match_count: int
    medium_confidence_match_count: int
    low_confidence_match_count: int
    no_match_count: int
    page_boundary_candidate_count: int
    high_confidence_boundary_count: int
    parable_boundary_candidate_present: bool
    glyph_variant_observation_count: int
    glyph_variant_occurrence_count: int
    canonical_corpus_active: bool
    trusted_as_canonical: bool
    page_boundary_status: str
    elapsed_milliseconds: dict[str, float]
    warnings: list[str] = field(default_factory=list)
