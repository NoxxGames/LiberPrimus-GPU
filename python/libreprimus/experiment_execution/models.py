"""Models for Stage 2F bounded CPU execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CPUExecutionManifest:
    payload: dict[str, Any]
    path: str
    sha256: str

    @property
    def manifest_id(self) -> str:
        return str(self.payload["manifest_id"])

    @property
    def execution_scope(self) -> str:
        return str(self.payload["execution_scope"])


@dataclass(frozen=True)
class ExecutionSafetyGateResult:
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
class CPUExecutionPlan:
    record_type: str
    plan_id: str
    manifest_id: str
    manifest_sha256: str
    generated_at_utc: str
    git_commit: str
    execution_enabled: bool
    execution_scope: str
    unsolved_execution_allowed: bool
    search_execution_enabled: bool
    candidate_generation_enabled: bool
    scoring_enabled: bool
    cuda_enabled: bool
    canonical_corpus_active: bool
    page_boundaries_final: bool
    trusted_as_canonical: bool
    transform_summary: dict[str, Any]
    input_summary: dict[str, Any]
    safety_gate_results: list[dict[str, Any]]
    output_paths: dict[str, str]
    result_store_preview: dict[str, Any]
    warnings: list[str]
    elapsed_ms: float


@dataclass(frozen=True)
class CPUExecutionResult:
    record_type: str
    result_id: str
    plan_id: str
    manifest_id: str
    manifest_sha256: str
    generated_at_utc: str
    git_commit: str
    execution_scope: str
    transform_id: str
    canonical_transform_id: str
    input_id: str
    output_normalized_text: str
    output_sha256: str
    expected_output_sha256: str | None
    match_status: str
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

