"""Stage 4D manifest loading and cap validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.bounded_numeric.loaders import load_yaml_payload
from libreprimus.bounded_numeric.models import EXPECTED_MANIFEST_IDS


def load_stage4b_manifests(manifest_dir: Path) -> list[dict[str, Any]]:
    """Load all Stage 4B disabled manifests in deterministic order."""

    if not manifest_dir.is_dir():
        raise FileNotFoundError(f"manifest_dir_missing: {manifest_dir}")
    manifests = [load_yaml_payload(path) for path in sorted(manifest_dir.glob("exp_stage4b_*.yaml"))]
    for manifest in manifests:
        validate_stage4b_manifest(manifest)
    return manifests


def validate_stage4b_manifest(manifest: dict[str, Any]) -> None:
    """Validate the Stage 4B disabled-manifest guardrails used by Stage 4D."""

    manifest_id = str(manifest.get("manifest_id") or "")
    if manifest_id not in EXPECTED_MANIFEST_IDS:
        raise ValueError(f"unexpected_stage4b_manifest:{manifest_id}")
    for field, expected in {
        "execution_enabled": False,
        "cuda_enabled": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "generated_outputs_committed": False,
    }.items():
        if manifest.get(field) is not expected:
            raise ValueError(f"{manifest_id}:{field}_must_be_{str(expected).lower()}")
    cap = int(manifest.get("candidate_count_upper_bound") or 0)
    if cap < 0 or cap > 100000:
        raise ValueError(f"{manifest_id}:candidate_cap_out_of_policy:{cap}")


def manifest_by_id(manifests: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Index loaded manifests by ID."""

    return {str(manifest.get("manifest_id")): manifest for manifest in manifests}


def cap_for(manifest: dict[str, Any]) -> int:
    """Return the declared candidate cap for a manifest."""

    return int(manifest.get("candidate_count_upper_bound") or 0)
