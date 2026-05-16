"""Load and validate Stage 2E exploratory experiment manifests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.experiments.models import ExploratoryManifest
from libreprimus.experiments.validation import validate_payload
from libreprimus.paths import repo_root
from libreprimus.transforms.registry import compute_sha256

FALSE_FIELDS = [
    "execution_enabled",
    "search_execution_enabled",
    "candidate_generation_enabled",
    "scoring_enabled",
    "cuda_enabled",
    "canonical_corpus_active",
    "page_boundaries_final",
    "trusted_as_canonical",
]


def load_exploratory_manifest(path: Path) -> ExploratoryManifest:
    resolved = path if path.is_absolute() else repo_root() / path
    payload = load_yaml_payload(resolved)
    validate_exploratory_manifest_payload(payload, source_text=resolved.read_text(encoding="utf-8"))
    return ExploratoryManifest(payload=payload, path=str(resolved), sha256=compute_sha256(resolved))


def load_yaml_payload(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Exploratory manifest must be a YAML mapping: {path}")
    return payload


def validate_exploratory_manifest_payload(payload: dict[str, Any], *, source_text: str = "") -> None:
    validate_payload(payload, "exploratory-experiment-manifest-v0.schema.json")
    validate_payload(payload["corpus_slice"], "exploratory-corpus-slice-v0.schema.json")
    validate_payload(payload["transform_plan"], "exploratory-transform-space-v0.schema.json")

    if payload.get("dry_run_only") is not True:
        raise ValueError("Stage 2E exploratory manifests require dry_run_only=true.")
    for field in FALSE_FIELDS:
        if payload.get(field) is not False:
            raise ValueError(f"Stage 2E exploratory manifests require {field}=false.")
    if "expected_candidate_count_upper_bound" not in payload:
        raise ValueError("Exploratory manifest requires expected_candidate_count_upper_bound.")
    corpus_slice = payload.get("corpus_slice", {})
    if (
        corpus_slice.get("slice_kind") == "future_unsolved_page_candidate"
        and corpus_slice.get("review_required") is not True
    ):
        raise ValueError("Future unsolved page candidate slices require review_required=true.")
    if _looks_like_raw_dump(source_text):
        raise ValueError("Exploratory manifest appears to include raw corpus data.")


def _looks_like_raw_dump(text: str) -> bool:
    return len(text) > 30000 or "data/raw/" in text or text.count("\n") > 1200
