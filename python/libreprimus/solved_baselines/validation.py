"""Validation for solved-baseline run manifests."""

from __future__ import annotations

from pathlib import Path

from libreprimus.paths import repo_root
from libreprimus.solved_baselines.manifest_loader import load_manifest
from libreprimus.solved_baselines.models import SolvedBaselineManifest
from libreprimus.transforms.registry import load_registry, resolve_transform
from libreprimus.transforms.validation import validate_registry


def _resolve_repo_path(path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else repo_root() / candidate


def validate_manifest(manifest: SolvedBaselineManifest) -> list[str]:
    errors: list[str] = []
    if manifest.canonical_corpus_active is not False:
        errors.append("Manifest canonical_corpus_active must be false.")
    if manifest.page_boundaries_final is not False:
        errors.append("Manifest page_boundaries_final must be false.")
    if manifest.search_enabled is not False:
        errors.append("Manifest search_enabled must be false.")
    if manifest.cuda_enabled is not False:
        errors.append("Manifest cuda_enabled must be false.")
    if manifest.scoring_enabled is not False:
        errors.append("Manifest scoring_enabled must be false.")
    registry_path = _resolve_repo_path("data/transform-registry/cpu-reference-transforms-v0.json")
    try:
        registry = load_registry(registry_path)
        if registry.registry_id != manifest.registry_id:
            errors.append(f"Registry ID mismatch: {registry.registry_id} != {manifest.registry_id}")
        if registry.sha256 != manifest.registry_sha256:
            errors.append("Registry SHA-256 mismatch.")
        errors.extend(validate_registry(registry))
        for group in manifest.fixture_groups:
            fixture_dir = _resolve_repo_path(group.fixture_dir)
            if not fixture_dir.is_dir():
                errors.append(f"{group.fixture_group_id}: fixture directory missing: {fixture_dir}")
                continue
            fixture_count = len(list(fixture_dir.glob("*.fixture.json")))
            if fixture_count != group.expected_fixture_count:
                errors.append(
                    f"{group.fixture_group_id}: expected {group.expected_fixture_count} fixtures, found {fixture_count}."
                )
            for transform_id in group.transform_ids:
                try:
                    resolve_transform(registry, transform_id)
                except KeyError as exc:
                    errors.append(f"{group.fixture_group_id}: unknown transform {transform_id}: {exc}")
    except (OSError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def validate_manifest_file(path: Path) -> list[str]:
    return validate_manifest(load_manifest(path))
