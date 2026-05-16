"""Models for experiment result-store records."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class HostMetadata:
    os: str
    platform: str
    machine: str
    processor: str
    python_version: str


@dataclass(frozen=True)
class ToolVersionMetadata:
    tool: str
    version: str


@dataclass(frozen=True)
class InputSourceMetadata:
    source_id: str
    sha256: str | None
    source_kind: str


@dataclass(frozen=True)
class ProfileMetadata:
    profile_id: str
    path: str
    sha256: str


@dataclass(frozen=True)
class FixtureCounts:
    total: int
    passed: int
    failed: int
    pending: int
    skipped: int

    def to_schema_dict(self) -> dict[str, int]:
        return {
            "total": self.total,
            "pass": self.passed,
            "fail": self.failed,
            "pending": self.pending,
            "skipped": self.skipped,
        }


@dataclass(frozen=True)
class TransformCounts:
    direct_translation_pass_count: int
    atbash_family_pass_count: int
    vigenere_pass_count: int
    prime_stream_pass_count: int


@dataclass(frozen=True)
class ResultStoreManifest:
    record_type: str
    manifest_id: str
    manifest_version: str
    description: str
    input_manifest_path: str
    input_manifest_sha256: str
    output_dir: str
    jsonl_output_path: str
    sqlite_output_path: str
    import_sources: list[str]
    canonical_corpus_active: bool
    page_boundaries_final: bool
    search_enabled: bool
    scoring_enabled: bool
    cuda_enabled: bool
    expected_run_kind: str
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ExperimentRunRecord:
    record_type: str
    run_id: str
    run_kind: str
    run_status: str
    manifest_id: str
    manifest_sha256: str
    registry_id: str
    registry_sha256: str
    git_commit: str
    branch: str
    created_at_utc: str
    completed_at_utc: str
    elapsed_ms: float
    host: dict[str, Any]
    tool_versions: dict[str, Any]
    input_sources: list[dict[str, Any]]
    profiles: list[dict[str, Any]]
    corpus_candidate_id: str
    canonical_corpus_active: bool
    page_boundaries_final: bool
    search_performed: bool
    scoring_used: bool
    cuda_used: bool
    gpu_required: bool
    random_seed: int | None
    fixture_counts: dict[str, int]
    transform_counts: dict[str, int]
    output_artifacts: list[str]
    warnings: list[str]
    trusted_as_canonical: bool
    notes: list[str]
    validation_status: str = "pass"


@dataclass(frozen=True)
class ExperimentEventRecord:
    record_type: str
    run_id: str
    event_index: int
    timestamp_utc: str
    level: str
    event_type: str
    message: str
    data: dict[str, Any]
    trusted_as_canonical: bool


@dataclass(frozen=True)
class ExperimentArtifactRecord:
    record_type: str
    run_id: str
    artifact_id: str
    artifact_kind: str
    path: str
    sha256: str
    size_bytes: int
    committed: bool
    ignored_by_git: bool
    notes: list[str]
    trusted_as_canonical: bool


@dataclass(frozen=True)
class ExperimentRunSummary:
    record_type: str
    summary_id: str
    generated_at_utc: str
    run_count: int
    pass_count: int
    fail_count: int
    partial_count: int
    pending_count: int
    skipped_count: int
    error_count: int
    run_kinds: list[str]
    canonical_corpus_active_any: bool
    search_performed_any: bool
    scoring_used_any: bool
    cuda_used_any: bool
    generated_artifact_count: int
    sqlite_database_path: str
    jsonl_path: str
    warnings: list[str]
    trusted_as_canonical: bool
