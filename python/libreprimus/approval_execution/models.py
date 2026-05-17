"""Models for Stage 2H approval-gated execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ApprovalExecutionRequest:
    payload: dict[str, Any]
    path: str
    sha256: str

    @property
    def request_id(self) -> str:
        return str(self.payload["request_id"])

    @property
    def execution_scope(self) -> str:
        return str(self.payload["execution_scope"])


@dataclass(frozen=True)
class ApprovalGateEvaluation:
    request: ApprovalExecutionRequest
    proposal: Any
    approval: Any
    approval_gate_status: str
    approved_for_execution: bool
    blocking_reasons: list[str]
    safety_gate_results: list[dict[str, Any]]
    execution_manifest_path: str | None
    warnings: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.approval_gate_status == "pass" and self.approved_for_execution


@dataclass(frozen=True)
class ApprovalGatedExecutionPlan:
    record_type: str
    plan_id: str
    request_id: str
    proposal_id: str
    proposal_sha256: str
    approval_id: str
    approval_status: str
    approved_for_execution: bool
    execution_scope: str
    generated_at_utc: str
    git_commit: str
    approval_gate_status: str
    blocking_reasons: list[str]
    safety_gate_results: list[dict[str, Any]]
    execution_manifest_preview: dict[str, Any]
    output_paths: dict[str, str]
    unsolved_execution_allowed: bool
    search_execution_enabled: bool
    candidate_generation_enabled: bool
    scoring_enabled: bool
    cuda_enabled: bool
    canonical_corpus_active: bool
    page_boundaries_final: bool
    trusted_as_canonical: bool
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ApprovalGatedExecutionResult:
    record_type: str
    result_id: str
    plan_id: str
    request_id: str
    proposal_id: str
    approval_id: str
    generated_at_utc: str
    git_commit: str
    execution_scope: str
    execution_performed: bool
    execution_status: str
    underlying_execution_result_ids: list[str]
    summary: dict[str, Any]
    search_performed: bool
    candidate_generation_performed: bool
    scoring_used: bool
    cuda_used: bool
    unsolved_execution_allowed: bool
    canonical_corpus_active: bool
    page_boundaries_final: bool
    trusted_as_canonical: bool
    warnings: list[str] = field(default_factory=list)
    elapsed_ms: float = 0.0

