"""Manifest loading and policy validation for Stage 4G."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.cookie_refresh.models import (
    DEFAULT_ALGORITHMS,
    DEFAULT_BYTE_VARIANTS,
    EXPERIMENT_ID,
    SUPPORTED_ALGORITHMS,
    SUPPORTED_BYTE_VARIANTS,
    CookieRefreshManifest,
)
from libreprimus.history.source_records import resolve_repo_path


def load_cookie_refresh_manifest(path: Path) -> CookieRefreshManifest:
    """Load the Stage 4B disabled cookie manifest as a Stage 4G executable scope."""

    payload = _read_yaml_mapping(resolve_repo_path(path))
    manifest_id = str(payload.get("manifest_id") or payload.get("experiment_id") or "")
    if manifest_id != EXPERIMENT_ID:
        raise ValueError(f"manifest_id must be {EXPERIMENT_ID}")
    if payload.get("cuda_enabled") is not False:
        raise ValueError("manifest cuda_enabled must be false")
    if payload.get("no_solve_claim") is not True:
        raise ValueError("manifest no_solve_claim must be true")
    if payload.get("canonical_corpus_active") is not False:
        raise ValueError("manifest canonical_corpus_active must be false")
    if payload.get("page_boundaries_final") is not False:
        raise ValueError("manifest page_boundaries_final must be false")
    if payload.get("generated_outputs_committed") is not False:
        raise ValueError("manifest generated_outputs_committed must be false")

    generation = payload.get("candidate_generation")
    generation = generation if isinstance(generation, dict) else {}

    cap = int(payload.get("candidate_count_upper_bound") or payload.get("candidate_count_cap") or 0)
    if cap <= 0 or cap > 100000:
        raise ValueError("manifest candidate_count_upper_bound must be in 1..100000")

    algorithms = _as_tuple(payload.get("algorithms") or generation.get("algorithms") or generation.get("algorithm") or DEFAULT_ALGORITHMS)
    unsupported_algorithms = sorted(set(algorithms) - SUPPORTED_ALGORITHMS)
    if unsupported_algorithms:
        raise ValueError(f"undeclared or unsupported algorithms: {', '.join(unsupported_algorithms)}")

    byte_variants = _as_tuple(payload.get("byte_variants") or generation.get("byte_variants") or DEFAULT_BYTE_VARIANTS)
    unsupported_variants = sorted(set(byte_variants) - SUPPORTED_BYTE_VARIANTS)
    if unsupported_variants:
        raise ValueError(f"undeclared or unsupported byte variants: {', '.join(unsupported_variants)}")

    if payload.get("exact_match_only", True) is not True:
        raise ValueError("manifest exact_match_only must be true")
    if payload.get("fuzzy_matching", generation.get("fuzzy_matching", False)) is not False:
        raise ValueError("manifest fuzzy_matching must be false")
    if payload.get("partial_matching", generation.get("partial_matching", False)) is not False:
        raise ValueError("manifest partial_matching must be false")
    if payload.get("broad_search", False) is not False:
        raise ValueError("manifest broad_search must be false")
    if payload.get("hashcat_used", generation.get("gpu_hashcat", False)) is not False:
        raise ValueError("manifest hashcat_used/gpu_hashcat must be false")
    if payload.get("cloud_execution", False) is not False:
        raise ValueError("manifest cloud_execution must be false")

    source_basis = _as_tuple(payload.get("source_basis") or ())
    if not source_basis:
        raise ValueError("manifest source_basis must be non-empty")

    return CookieRefreshManifest(
        manifest_id=manifest_id,
        candidate_count_upper_bound=cap,
        source_basis=source_basis,
        byte_variants=byte_variants,
        algorithms=algorithms,
        payload=payload,
    )


def validate_cookie_refresh_manifest(path: Path) -> tuple[dict[str, Any], list[str]]:
    """Validate a Stage 4G cookie refresh manifest view."""

    try:
        manifest = load_cookie_refresh_manifest(path)
    except Exception as exc:  # noqa: BLE001
        return {}, [str(exc)]
    return {
        "manifest_id": manifest.manifest_id,
        "candidate_count_upper_bound": manifest.candidate_count_upper_bound,
        "byte_variant_count": len(manifest.byte_variants),
        "algorithms": list(manifest.algorithms),
        "exact_match_only": True,
        "fuzzy_matching": False,
        "partial_matching": False,
        "hashcat_used": False,
        "cuda_used": False,
        "no_solve_claim": True,
    }, []


def _as_tuple(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,)
    if isinstance(value, list | tuple):
        return tuple(str(item) for item in value)
    return tuple(str(item) for item in value) if value else ()


def _read_yaml_mapping(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"YAML file must be a mapping: {path}")
    return payload
