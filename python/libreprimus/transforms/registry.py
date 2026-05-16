"""Load CPU reference transform registries."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from libreprimus.paths import repo_root
from libreprimus.transforms.models import TransformDefinition, TransformRegistry

DEFAULT_REGISTRY_PATH = Path("data/transform-registry/cpu-reference-transforms-v0.json")


def compute_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_sha_lock(path: Path) -> str | None:
    lock_path = path.with_suffix(".sha256")
    if not lock_path.is_file():
        return None
    return lock_path.read_text(encoding="utf-8").split()[0]


def load_registry(path: Path | None = None, *, validate_lock: bool = True) -> TransformRegistry:
    registry_path = repo_root() / (path or DEFAULT_REGISTRY_PATH)
    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    actual_sha = compute_sha256(registry_path)
    expected_sha = _load_sha_lock(registry_path)
    if validate_lock and expected_sha is not None and actual_sha != expected_sha:
        raise ValueError(f"Transform registry SHA-256 lock mismatch for {registry_path}.")
    transforms = [_definition_from_payload(item) for item in payload.get("transforms", [])]
    return TransformRegistry(
        registry_id=str(payload["registry_id"]),
        registry_kind=str(payload["registry_kind"]),
        status=str(payload["status"]),
        canonical_corpus_active=bool(payload["canonical_corpus_active"]),
        search_enabled=bool(payload["search_enabled"]),
        cuda_enabled=bool(payload["cuda_enabled"]),
        scoring_enabled=bool(payload["scoring_enabled"]),
        transforms=transforms,
        sha256=actual_sha,
    )


def _definition_from_payload(payload: dict[str, Any]) -> TransformDefinition:
    return TransformDefinition(
        transform_id=str(payload["transform_id"]),
        transform_version=str(payload["transform_version"]),
        method_family=str(payload["method_family"]),
        aliases=[str(item) for item in payload.get("aliases", [])],
        formula=str(payload["formula"]),
        parameter_schema=dict(payload.get("parameter_schema", {})),
        supports_cpu_reference=bool(payload["supports_cpu_reference"]),
        supports_gpu=bool(payload["supports_gpu"]),
        search_enabled=bool(payload["search_enabled"]),
        scoring_enabled=bool(payload["scoring_enabled"]),
        fixture_baseline_supported=bool(payload["fixture_baseline_supported"]),
        implemented_module=payload.get("implemented_module"),
        provenance_notes=[str(item) for item in payload.get("provenance_notes", [])],
        known_fixture_sets=[str(item) for item in payload.get("known_fixture_sets", [])],
        supports_inverse=bool(payload.get("supports_inverse", False)),
        alias_of=payload.get("alias_of"),
        canonical_transform_id=payload.get("canonical_transform_id"),
        implemented_as_alias=bool(payload.get("implemented_as_alias", False)),
        equivalence=payload.get("equivalence"),
    )


def transform_by_id(registry: TransformRegistry) -> dict[str, TransformDefinition]:
    return {definition.transform_id: definition for definition in registry.transforms}


def resolve_transform(registry: TransformRegistry, transform_id: str) -> TransformDefinition:
    definitions = transform_by_id(registry)
    if transform_id not in definitions:
        raise KeyError(f"Unknown transform_id: {transform_id}")
    definition = definitions[transform_id]
    if definition.alias_of:
        if definition.alias_of not in definitions:
            raise KeyError(f"Alias target missing for {transform_id}: {definition.alias_of}")
        return definitions[definition.alias_of]
    return definition
