"""Models for Stage 2G proposal review records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ExperimentProposal:
    payload: dict[str, Any]
    path: str
    sha256: str

    @property
    def proposal_id(self) -> str:
        return str(self.payload["proposal_id"])


@dataclass(frozen=True)
class ApprovalRecord:
    payload: dict[str, Any]
    path: str
    sha256: str

    @property
    def approval_status(self) -> str:
        return str(self.payload["approval_status"])


@dataclass(frozen=True)
class ApprovalGateResult:
    proposal_id: str
    approval_status: str
    approved_for_execution: bool
    execution_blocked: bool
    reason: str


@dataclass(frozen=True)
class ReviewPacket:
    record_type: str
    packet_id: str
    proposal_id: str
    proposal_sha256: str
    generated_at_utc: str
    git_commit: str
    proposal_summary: dict[str, Any]
    dry_run_summary: dict[str, Any]
    safety_gate_summary: dict[str, Any]
    risk_summary: dict[str, Any]
    approval_status: str
    approved_for_execution: bool
    execution_blocked: bool
    warnings: list[str]
    recommended_decision: str
    output_paths: dict[str, str]
    canonical_corpus_active: bool
    page_boundaries_final: bool
    trusted_as_canonical: bool

