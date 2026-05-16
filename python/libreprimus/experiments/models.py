"""Models for Stage 2E exploratory experiment dry-run planning."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ExploratoryManifest:
    payload: dict[str, Any]
    path: str
    sha256: str

    @property
    def manifest_id(self) -> str:
        return str(self.payload["manifest_id"])

    @property
    def transform_family(self) -> str:
        return str(self.payload["transform_plan"]["transform_family"])


@dataclass(frozen=True)
class CandidateEstimate:
    transform_family: str
    candidate_count: int
    candidate_count_formula: str
    parameter_summary: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SafetyGateResult:
    gate_id: str
    gate_name: str
    required_value: Any
    actual_value: Any
    status: str
    severity: str
    message: str

    @property
    def is_failure(self) -> bool:
        return self.status == "fail" or self.severity == "error"

    @property
    def is_warning(self) -> bool:
        return self.status == "warning" or self.severity == "warning"


@dataclass(frozen=True)
class DryRunPlan:
    record_type: str
    plan_id: str
    manifest_id: str
    manifest_sha256: str
    generated_at_utc: str
    git_commit: str
    dry_run_only: bool
    execution_enabled: bool
    search_execution_enabled: bool
    candidate_generation_enabled: bool
    scoring_enabled: bool
    cuda_enabled: bool
    canonical_corpus_active: bool
    page_boundaries_final: bool
    trusted_as_canonical: bool
    corpus_slice_summary: dict[str, Any]
    transform_space_summary: dict[str, Any]
    candidate_count_estimate: int
    candidate_count_upper_bound: int
    safety_gate_results: list[dict[str, Any]]
    warnings: list[str]
    output_paths: dict[str, str]
    result_store_preview: dict[str, Any]
    elapsed_ms: float
