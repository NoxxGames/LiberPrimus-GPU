"""Models for Stage 2J bounded CPU experiment automation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class OperatorPolicy:
    payload: dict[str, Any]
    path: str
    sha256: str

    @property
    def policy_id(self) -> str:
        return str(self.payload["policy_id"])

    @property
    def max_candidate_count(self) -> int:
        return int(self.payload["limits"]["max_candidate_count"])

    @property
    def max_estimated_runtime_seconds(self) -> int:
        return int(self.payload["limits"]["max_estimated_runtime_seconds"])

    @property
    def max_generated_output_mb(self) -> float:
        return float(self.payload["limits"]["max_generated_output_mb"])


@dataclass(frozen=True)
class BoundedExperimentQueue:
    payload: dict[str, Any]
    path: str
    sha256: str

    @property
    def queue_id(self) -> str:
        return str(self.payload["queue_id"])

    @property
    def policy_id(self) -> str:
        return str(self.payload["policy_id"])

    @property
    def items(self) -> list[dict[str, Any]]:
        return [dict(item) for item in self.payload.get("items", [])]


@dataclass(frozen=True)
class PolicyCheckResult:
    item_id: str
    policy_id: str
    status: str
    checks: list[dict[str, str]]
    blocking_reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.status == "pass"


@dataclass(frozen=True)
class BoundedAutoRunResult:
    record_type: str
    item_id: str
    queue_id: str
    policy_id: str
    generated_at_utc: str
    git_commit: str
    execution_performed: bool
    candidate_count: int
    output_paths: dict[str, str]
    summary: dict[str, Any]
    search_performed: bool
    scoring_used: bool
    cuda_used: bool
    solve_claim_made: bool
    canonical_corpus_active: bool
    page_boundaries_final: bool
    trusted_as_canonical: bool
    execution_status: str = "skipped"
    deferred_reason: str | None = None
    warnings: list[str] = field(default_factory=list)
