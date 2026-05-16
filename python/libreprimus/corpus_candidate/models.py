"""Models for Stage 0E corpus candidate records."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


def to_jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {key: to_jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]
    return value


@dataclass(frozen=True)
class CorpusGenerationWarning:
    record_type: str
    corpus_candidate_id: str
    warning_code: str
    severity: str
    source_line: int | None
    source_column: int | None
    message: str
    raw_context: str
    trusted_as_canonical: bool = False


@dataclass(frozen=True)
class CorpusTokenRecord:
    record_type: str
    corpus_candidate_id: str
    source_id: str
    source_sha256: str
    physical_line_number: int
    logical_line_index: int
    token_index_global: int
    token_index_in_line: int
    raw_text: str
    token_kind: str
    raw_glyph: str | None
    normalized_glyph: str | None
    index29: int | None
    prime_value: int | None
    latin_label: str | None
    variant_mapping_applied: bool
    variant_source: str | None
    separator_class: str | None
    source_column_start: int | None
    source_column_end: int | None
    page_candidate_ids: list[str]
    trusted_as_canonical: bool = False
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class CorpusLineRecord:
    record_type: str
    corpus_candidate_id: str
    source_id: str
    source_sha256: str
    physical_line_number_start: int
    physical_line_number_end: int
    logical_line_index: int
    raw_text: str
    token_count: int
    rune_count: int
    separator_counts: dict[str, int]
    rune_indices: list[int]
    prime_values: list[int]
    line_signature_sha256: str
    page_candidate_ids: list[str]
    trusted_as_canonical: bool = False
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class CorpusPageCandidateRecord:
    record_type: str
    corpus_candidate_id: str
    candidate_page_id: str
    candidate_page_label: str | None
    candidate_local_page_index: int | None
    candidate_global_page_index: int | None
    source: str
    confidence: str
    confidence_score: float
    evidence: list[str]
    start_token_index: int | None
    end_token_index: int | None
    start_logical_line_index: int | None
    end_logical_line_index: int | None
    start_physical_line_number: int | None
    end_physical_line_number: int | None
    canonical_page_boundary: bool = False
    page_boundaries_final: bool = False
    trusted_as_canonical: bool = False
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class CorpusCandidateManifest:
    record_type: str
    corpus_candidate_id: str
    source_transcript_id: str
    source_transcript_sha256: str
    source_transcript_local_path: str
    gematria_profile_id: str
    gematria_profile_sha256: str
    separator_grammar_id: str
    separator_grammar_sha256: str
    glyph_variant_profile_id: str
    glyph_variant_profile_sha256: str
    generated_at_utc: str
    git_commit: str
    generator_version: str
    canonical_corpus_candidate: bool
    canonical_corpus_active: bool
    page_boundaries_final: bool
    trusted_as_canonical: bool
    line_count: int
    token_count: int
    rune_token_count: int
    separator_token_count: int
    unknown_symbol_count: int
    warning_count: int
    page_candidate_count: int
    notes: list[str]


@dataclass(frozen=True)
class CorpusCandidateSummary:
    record_type: str
    corpus_candidate_id: str
    physical_line_count: int
    logical_line_count: int
    token_count: int
    rune_token_count: int
    separator_token_count: int
    numeric_literal_count: int
    unknown_symbol_count: int
    variant_mapped_token_count: int
    page_candidate_count: int
    warning_count: int
    canonical_corpus_candidate: bool
    canonical_corpus_active: bool
    page_boundaries_final: bool
    trusted_as_canonical: bool
    elapsed_milliseconds: dict[str, float]
