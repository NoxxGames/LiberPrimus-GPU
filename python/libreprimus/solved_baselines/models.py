"""Models for solved-baseline run manifests and outputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class FixtureGroup:
    fixture_group_id: str
    fixture_dir: str
    method_family: str
    transform_ids: list[str]
    expected_fixture_count: int
    expected_pass_count: int
    allow_pending: bool


@dataclass(frozen=True)
class SolvedBaselineManifest:
    record_type: str
    manifest_id: str
    manifest_version: str
    description: str
    registry_id: str
    registry_sha256: str
    corpus_candidate_id: str
    canonical_corpus_active: bool
    page_boundaries_final: bool
    search_enabled: bool
    cuda_enabled: bool
    scoring_enabled: bool
    fixture_groups: list[FixtureGroup]
    output_dir: str
    allow_pending: bool
    allow_warnings: bool
    require_all_pass: bool
    expected_counts: dict[str, int]
    provenance: dict[str, Any]
    notes: list[str] = field(default_factory=list)
    manifest_sha256: str = ""


@dataclass(frozen=True)
class ManifestRunRecord:
    record_type: str
    manifest_id: str
    manifest_sha256: str
    registry_id: str
    registry_sha256: str
    fixture_group_id: str
    fixture_id: str
    transform_id: str | None
    canonical_transform_id: str | None
    method_family: str
    match_status: str
    mismatch_reason: str | None
    search_performed: bool
    cuda_used: bool
    scoring_used: bool
    canonical_corpus_active: bool
    page_boundaries_final: bool
    trusted_as_canonical: bool
    source_record: dict[str, Any]


@dataclass(frozen=True)
class ManifestRunSummary:
    record_type: str
    manifest_id: str
    manifest_sha256: str
    registry_id: str
    registry_sha256: str
    fixture_group_count: int
    fixture_count: int
    pass_count: int
    fail_count: int
    pending_count: int
    skipped_count: int
    direct_translation_pass_count: int
    atbash_family_pass_count: int
    vigenere_pass_count: int
    prime_stream_pass_count: int
    search_performed_any: bool
    cuda_used_any: bool
    scoring_used_any: bool
    canonical_corpus_active: bool
    page_boundaries_final: bool
    elapsed_ms: float
    warnings: list[str]
