"""Models for CPU reference transform registry dispatch."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class TransformDefinition:
    transform_id: str
    transform_version: str
    method_family: str
    aliases: list[str]
    formula: str
    parameter_schema: dict[str, Any]
    supports_cpu_reference: bool
    supports_gpu: bool
    search_enabled: bool
    scoring_enabled: bool
    fixture_baseline_supported: bool
    implemented_module: str | None
    provenance_notes: list[str]
    known_fixture_sets: list[str]
    supports_inverse: bool = False
    alias_of: str | None = None
    canonical_transform_id: str | None = None
    implemented_as_alias: bool = False
    equivalence: str | None = None


@dataclass(frozen=True)
class TransformRegistry:
    registry_id: str
    registry_kind: str
    status: str
    canonical_corpus_active: bool
    search_enabled: bool
    cuda_enabled: bool
    scoring_enabled: bool
    transforms: list[TransformDefinition]
    sha256: str


@dataclass(frozen=True)
class TransformParameters:
    transform_id: str
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TransformExecutionContext:
    transform_id: str
    parameters: dict[str, Any]
    tokens: list[dict[str, Any]]
    payload_checks: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class TransformWarning:
    message: str
    severity: str = "warning"


@dataclass(frozen=True)
class TransformResult:
    transform_id: str
    canonical_transform_id: str
    transform_version: str
    parameters: dict[str, Any]
    decoded_index_formula: str | None
    decoded_normalized_plaintext: str | None
    decoded_normalized_plaintext_sha256: str | None
    rune_count: int
    numeric_literal_count: int
    separator_count: int
    warnings: list[str]
    search_performed: bool
    cuda_used: bool
    scoring_used: bool
    key_text: str | None = None
    key_indices: list[int] = field(default_factory=list)
    skip_rule_applied_count: int = 0
    prime_values_used_count: int = 0
    stream_values_used_count: int = 0
    first_prime_values: list[int] = field(default_factory=list)
    first_stream_values_mod29: list[int] = field(default_factory=list)
    payload_check_results: list[dict[str, Any]] = field(default_factory=list)
