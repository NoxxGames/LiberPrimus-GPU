"""Models for Stage 2I approval-readiness packets."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ReadinessAnalysis:
    proposal: Any
    approval: Any | None
    readiness_status: str
    approval_status: str
    real_unsolved_material_touched: bool
    candidate_count_estimate: int
    candidate_count_upper_bound: int
    blocking_conditions: list[str]
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ApprovalReadinessPacket:
    record_type: str
    packet_id: str
    proposal_id: str
    proposal_sha256: str
    generated_at_utc: str
    git_commit: str
    proposal_status: str
    approval_status: str
    approved_for_execution: bool
    execution_enabled: bool
    search_execution_enabled: bool
    candidate_generation_enabled: bool
    scoring_enabled: bool
    cuda_enabled: bool
    canonical_corpus_active: bool
    page_boundaries_final: bool
    trusted_as_canonical: bool
    real_unsolved_material_touched: bool
    corpus_slice_summary: dict[str, Any]
    transform_space_summary: dict[str, Any]
    candidate_count_estimate: int
    candidate_count_upper_bound: int
    safety_gate_summary: dict[str, Any]
    review_checklist_summary: dict[str, Any]
    approval_requirements: list[str]
    blocking_conditions: list[str]
    risk_summary: dict[str, Any]
    recommended_human_decision: str
    generated_output_preview: dict[str, str]
    result_store_preview: dict[str, Any]
    warnings: list[str]
    notes: list[str]
