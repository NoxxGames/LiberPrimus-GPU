"""Models for transcript source parsing."""

from __future__ import annotations

from dataclasses import dataclass, field

RTKD_SOURCE_ID = "rtkd-master-transcription"
SCREAM314_SOURCE_ID = "scream314-liber-primus-md"


@dataclass(frozen=True)
class TranscriptLineRecord:
    record_type: str
    source_id: str
    source_sha256: str
    source_local_path: str
    physical_line_number: int
    raw_text: str
    stripped_text: str
    rune_glyphs: list[str]
    rune_count: int
    separator_counts: dict[str, int]
    raw_separator_characters: list[str]
    has_page_marker: bool
    has_section_marker: bool
    inferred_part_candidate: str | None
    inferred_local_page_candidate: int | None
    page_marker_raw: str | None
    parse_warnings: list[str] = field(default_factory=list)
    trusted_as_canonical: bool = False


@dataclass(frozen=True)
class TranscriptSourceSummary:
    record_type: str
    source_id: str
    source_sha256: str
    source_local_path: str
    physical_line_count: int
    rune_line_count: int
    rune_count: int
    page_marker_count: int
    section_marker_count: int
    parse_warning_count: int
    trusted_as_canonical: bool
    canonical_corpus_active: bool


@dataclass(frozen=True)
class Scream314ReferenceRecord:
    record_type: str
    source_id: str
    source_sha256: str
    source_local_path: str
    physical_line_number: int
    raw_text: str
    reference_kind: str
    page_label: str | None
    part_label: str | None
    solved_section_title: str | None
    method_keywords: list[str]
    trusted_as_canonical: bool


@dataclass(frozen=True)
class Scream314ReferenceSummary:
    record_type: str
    source_id: str
    source_sha256: str
    source_local_path: str
    physical_line_count: int
    reference_record_count: int
    page_label_count: int
    lp2_page_count_statement: str | None
    trusted_as_canonical: bool
    canonical_corpus_active: bool
