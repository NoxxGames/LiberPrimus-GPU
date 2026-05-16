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
    transcript_view_name: str | None = None
    transcript_offset_start: int | None = None
    transcript_offset_end: int | None = None
    transcript_logical_line_start: int | None = None
    transcript_logical_line_end: int | None = None
    transcript_physical_line_start: int | None = None
    transcript_physical_line_end: int | None = None
    confidence_reason: str = ""
    previous_pair_distance: int | None = None
    next_pair_distance: int | None = None


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
    gap_reason: str | None = None
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
    explicit_marker: bool = False
    anchor_supported: bool = False
    aligned_pair_count_near_boundary: int = 0
    no_match_count_near_boundary: int = 0
    downgraded_from_previous_policy: bool = False
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


@dataclass(frozen=True)
class TranscriptViewRecord:
    record_type: str
    source_id: str
    source_sha256: str
    view_name: str
    view_record_index: int
    raw_text_span: str
    flattened_rune_sequence: str
    normalized_rune_sequence: str
    decimal_index_sequence: list[int]
    rune_count: int
    source_line_start: int | None
    source_line_end: int | None
    source_offset_start: int | None
    source_offset_end: int | None
    separator_profile: dict[str, int]
    trusted_as_canonical: bool = False
    raw_marker_text: str | None = None
    offset_map: list[dict[str, int | str | None]] = field(default_factory=list)


@dataclass(frozen=True)
class TranscriptViewsSummary:
    record_type: str
    source_id: str
    source_sha256: str
    physical_line_count: int
    logical_line_count: int
    stream_rune_count: int
    explicit_marker_count: int
    candidate_lp2_span_found: bool
    trusted_as_canonical: bool = False


@dataclass(frozen=True)
class AlignmentGapDiagnostic:
    record_type: str
    source_id: str
    pastebin_source_sha256: str
    transcript_source_id: str
    transcript_source_sha256: str
    pair_index: int
    rune_count: int
    word_count: int
    word_length_sequence: list[int]
    flattened_rune_sha256: str
    normalized_rune_sha256: str
    decimal_index_sha256: str
    first_rune: str | None
    last_rune: str | None
    first_prime_value: int | None
    last_prime_value: int | None
    source_rune_line_number: int | None
    source_prime_line_number: int | None
    previous_pair_match_status: str | None
    next_pair_match_status: str | None
    empty_pair: bool
    contains_variant_glyph: bool
    candidate_reason_labels: list[str]
    explanation: str
    trusted_as_canonical: bool = False


@dataclass(frozen=True)
class AlignmentGapSummary:
    record_type: str
    total_pairs: int
    matched_pairs: int
    no_match_pairs: int
    low_confidence_pairs: int
    gap_reason_counts: dict[str, int]
    empty_pair_count: int
    pairs_with_variant_glyphs: int
    pairs_with_subsequence_matches_after_new_passes: int
    unresolved_pairs: int
    top_20_unresolved_pair_indices: list[int]
    timing_ms: dict[str, float]
    trusted_as_canonical: bool = False


@dataclass(frozen=True)
class PageBoundaryConfidenceAudit:
    record_type: str
    candidate_page_label: str | None
    candidate_local_page_index: int | None
    start_pair_index: int | None
    end_pair_index: int | None
    confidence: str
    previous_policy_confidence: str
    downgraded_from_previous_policy: bool
    explicit_marker: bool
    anchor_supported: bool
    aligned_pair_count_near_boundary: int
    no_match_count_near_boundary: int
    empty_pair_only: bool
    canonical_page_boundary: bool
    evidence: list[str]
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class PageBoundaryAuditSummary:
    record_type: str
    total_boundary_candidates: int
    high_count: int
    medium_count: int
    low_count: int
    none_count: int
    overgeneration_warning: bool
    candidates_exceed_expected_lp2_page_count: bool
    candidates_with_explicit_marker: int
    candidates_with_anchor: int
    candidates_from_empty_pair_only: int
    candidates_downgraded_from_previous_policy: int
    parable_candidate_confidence: str | None
    canonical_page_boundary_all_false: bool
    trusted_as_canonical: bool = False


@dataclass(frozen=True)
class Stage0DFollowupAlignmentSummary:
    record_type: str
    source_id: str
    pastebin_source_sha256: str
    transcript_source_id: str
    transcript_source_sha256: str
    transcript_physical_line_count: int
    transcript_logical_line_count: int
    transcript_rune_stream_length: int
    pastebin_line_pair_count: int
    alignment_record_count: int
    exact_count: int
    high_count: int
    medium_count: int
    low_count: int
    none_count: int
    baseline_none_count: int
    no_match_reduction: int
    logical_line_match_count: int
    stream_subsequence_match_count: int
    decimal_index_match_count: int
    variant_normalized_match_count: int
    gap_reason_counts: dict[str, int]
    boundary_high_count: int
    boundary_medium_count: int
    boundary_low_count: int
    boundary_none_count: int
    overgeneration_warning: bool
    glyph_variant_observation_count: int
    canonical_corpus_active: bool
    page_boundary_status: str
    timing_ms: dict[str, float]
    trusted_as_canonical: bool = False
