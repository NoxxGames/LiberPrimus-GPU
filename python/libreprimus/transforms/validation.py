"""Validation for CPU reference transform registries."""

from __future__ import annotations

import importlib
from pathlib import Path

from jsonschema import validate

from libreprimus.paths import repo_root
from libreprimus.transforms.models import TransformRegistry
from libreprimus.transforms.registry import resolve_transform, transform_by_id


def validate_registry(registry: TransformRegistry) -> list[str]:
    errors: list[str] = []
    if registry.canonical_corpus_active is not False:
        errors.append("Registry canonical_corpus_active must be false.")
    if registry.search_enabled is not False:
        errors.append("Registry search_enabled must be false.")
    if registry.cuda_enabled is not False:
        errors.append("Registry cuda_enabled must be false.")
    if registry.scoring_enabled is not False:
        errors.append("Registry scoring_enabled must be false.")
    ids = [definition.transform_id for definition in registry.transforms]
    if len(ids) != len(set(ids)):
        errors.append("Transform IDs must be unique.")
    definitions = transform_by_id(registry)
    for definition in registry.transforms:
        if definition.alias_of and definition.alias_of not in definitions:
            errors.append(f"{definition.transform_id}: alias target missing: {definition.alias_of}")
        if definition.supports_cpu_reference is not True:
            errors.append(f"{definition.transform_id}: supports_cpu_reference must be true.")
        if definition.supports_gpu is not False:
            errors.append(f"{definition.transform_id}: supports_gpu must be false.")
        if definition.search_enabled is not False:
            errors.append(f"{definition.transform_id}: search_enabled must be false.")
        if definition.scoring_enabled is not False:
            errors.append(f"{definition.transform_id}: scoring_enabled must be false.")
        if not definition.alias_of and not definition.implemented_module:
            errors.append(f"{definition.transform_id}: implementation module is required.")
        if definition.implemented_module:
            module_name, _, attr = definition.implemented_module.rpartition(".")
            try:
                module = importlib.import_module(module_name)
                if not hasattr(module, attr):
                    errors.append(f"{definition.transform_id}: implementation attribute missing.")
            except ImportError as exc:
                errors.append(f"{definition.transform_id}: implementation import failed: {exc}")
        for fixture_set in definition.known_fixture_sets:
            fixture_dir = repo_root() / "data/fixtures/solved-pages" / fixture_set
            if not fixture_dir.is_dir():
                errors.append(f"{definition.transform_id}: fixture set path missing: {fixture_dir}")
    try:
        resolve_transform(registry, "phi_prime_stream")
    except KeyError as exc:
        errors.append(str(exc))
    return errors


def validate_parameters(schema: dict, parameters: dict) -> None:
    validate(instance=parameters, schema=schema)


def validate_registry_file(path: Path) -> list[str]:
    from libreprimus.transforms.registry import load_registry

    return validate_registry(load_registry(path))
