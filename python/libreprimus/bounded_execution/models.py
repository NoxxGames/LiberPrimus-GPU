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
