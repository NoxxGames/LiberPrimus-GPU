"""Models for Stage 3A bounded CPU candidate execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class MissingReviewableSliceInput(ValueError):
    """Raised when a queue item cannot resolve a safe input index stream."""


@dataclass(frozen=True)
class InputSlice:
    slice_id: str
    corpus_candidate_id: str
    page_candidate_id: str
    index29_values: list[int]
    source_metadata: dict[str, Any]
    warnings: list[str] = field(default_factory=list)

    @property
    def input_length(self) -> int:
        return len(self.index29_values)


@dataclass(frozen=True)
class BoundedCandidateRecord:
    record_type: str
    run_id: str
    queue_item_id: str
    transform_family: str
    transform_id: str
    transform_parameters: dict[str, Any]
    candidate_index: int
    input_slice_id: str
    output_normalized_text: str
    output_preview: str
    output_sha256: str
    score_summary: dict[str, Any]
    ranking_features: dict[str, Any]
    search_performed: bool
    scoring_used: bool
    cuda_used: bool
    canonical_corpus_active: bool
    page_boundaries_final: bool
    solve_claim: bool
    trusted_as_canonical: bool
    warnings: list[str] = field(default_factory=list)
    key_text: str | None = None
    key_indices: list[int] | None = None
    evidence_family: str | None = None
    calibrated_confidence_label: str | None = None
    crib_hits: list[str] | None = None
    crib_hit_count: int | None = None
    calibration_position: dict[str, Any] | None = None
    base_transform_id: str | None = None
    base_transform_family: str | None = None
    reset_mode: str | None = None
    advance_mode: str | None = None
    transformable_token_count: int | None = None
    metadata_support_status: dict[str, Any] | None = None
    stream_variant: str | None = None
    offset: int | None = None
    direction: str | None = None
    stream_signature_sha256: str | None = None
    exponent_sequence_id: str | None = None
    exponent_sequence: list[int] | None = None


@dataclass(frozen=True)
class BoundedRunSummary:
    record_type: str
    run_id: str
    queue_item_id: str
    input_slice_id: str
    input_length: int
    candidate_count: int
    caesar_candidate_count: int
    affine_candidate_count: int
    top_k_count: int
    top_candidate: dict[str, Any]
    output_paths: dict[str, str]
    generated_outputs_ignored: bool
    result_store_preview: dict[str, Any]
    search_performed: bool
    scoring_used: bool
    cuda_used: bool
    canonical_corpus_active: bool
    page_boundaries_final: bool
    solve_claim: bool
    trusted_as_canonical: bool
    warnings: list[str] = field(default_factory=list)
    vigenere_candidate_count: int | None = None
    expected_candidate_count: int | None = None
    executed_candidate_count: int | None = None
    deferred_candidate_count: int | None = None
    key_count: int | None = None
    reset_modes: list[str] | None = None
    advance_modes: list[str] | None = None
    confidence_distribution: dict[str, int] | None = None
    prime_candidate_count: int | None = None
    reset_advance_candidate_count: int | None = None
    negative_control_count: int | None = None
    metadata_support_status: dict[str, Any] | None = None
    mersenne_candidate_count: int | None = None
    stream_variants: list[str] | None = None
    directions: list[str] | None = None
    unique_stream_signature_count: int | None = None
    duplicate_stream_signature_count: int | None = None
