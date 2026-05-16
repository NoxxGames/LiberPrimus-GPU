"""Models for solved-page golden fixtures and reproduction records."""

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
class SpanSelector:
    selector_kind: str
    source: str
    start_logical_line_index: int | None = None
    end_logical_line_index: int | None = None
    start_token_index: int | None = None
    end_token_index: int | None = None
    page_candidate_ids: list[str] = field(default_factory=list)
    notes: str = ""


@dataclass(frozen=True)
class SolvedPageFixture:
    record_type: str
    fixture_id: str
    fixture_version: str
    solved_section_title: str
    solved_section_aliases: list[str]
    method_family: str
    method_status: str
    transform_chain: list[Any]
    direct_translation_expected: bool
    in_scope_for_stage: bool
    source_transcript_id: str
    source_transcript_sha256: str
    solved_reference_source_id: str
    solved_reference_sha256: str
    gematria_profile_id: str
    gematria_profile_sha256: str
    separator_grammar_id: str
    separator_grammar_sha256: str
    glyph_variant_profile_id: str
    glyph_variant_profile_sha256: str
    corpus_candidate_id: str
    corpus_candidate_status: str
    span_selector: SpanSelector
    span_status: str
    expected_normalized_plaintext: str | None
    expected_normalized_plaintext_sha256: str | None
    expected_rune_count: int | None
    expected_numeric_literal_count: int | None
    expected_separator_policy: str
    expected_known_caveats: list[str]
    payload_checks: list[dict[str, Any]]
    trusted_as_canonical: bool
    canonical_corpus_active: bool
    page_boundaries_final: bool
    notes: list[str]


@dataclass(frozen=True)
class ReproductionRecord:
    record_type: str
    fixture_id: str
    corpus_candidate_id: str
    generated_at_utc: str
    git_commit: str
    method_family: str
    transform_chain: list[Any]
    decoded_index_formula: str | None
    transform_parameters: dict[str, Any]
    key_text: str | None
    key_indices: list[int]
    skip_rule_applied_count: int
    prime_values_used_count: int
    stream_values_used_count: int
    first_prime_values: list[int]
    first_stream_values_mod29: list[int]
    payload_check_results: list[dict[str, Any]]
    span_selector: SpanSelector
    decoded_normalized_plaintext: str | None
    decoded_normalized_plaintext_sha256: str | None
    expected_normalized_plaintext_sha256: str | None
    match_status: str
    mismatch_reason: str | None
    rune_count: int
    numeric_literal_count: int
    separator_count: int
    warnings: list[str]
    trusted_as_canonical: bool = False
    canonical_corpus_active: bool = False
    page_boundaries_final: bool = False


@dataclass(frozen=True)
class ReproductionSummary:
    record_type: str
    fixture_set_id: str
    generated_at_utc: str
    git_commit: str
    fixture_count: int
    pass_count: int
    fail_count: int
    pending_count: int
    skipped_count: int
    direct_translation_pass_count: int
    direct_translation_fail_count: int
    canonical_corpus_active: bool
    page_boundaries_final: bool
    warnings: list[str]
    elapsed_ms: float
