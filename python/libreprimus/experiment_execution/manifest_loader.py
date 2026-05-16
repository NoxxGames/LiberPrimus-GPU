"""Load and validate Stage 2F CPU execution manifests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.experiment_execution.models import CPUExecutionManifest
from libreprimus.experiment_execution.validation import validate_payload
from libreprimus.paths import repo_root
from libreprimus.transforms.registry import compute_sha256

ALLOWED_EXECUTION_SCOPES = {
    "synthetic_only",
    "solved_fixture_only",
    "synthetic_and_solved_fixture_only",
}

FALSE_FIELDS = [
    "unsolved_execution_allowed",
    "search_execution_enabled",
    "candidate_generation_enabled",
    "scoring_enabled",
    "cuda_enabled",
    "canonical_corpus_active",
    "page_boundaries_final",
    "trusted_as_canonical",
]


def load_cpu_execution_manifest(path: Path) -> CPUExecutionManifest:
    resolved = path if path.is_absolute() else repo_root() / path
    payload = load_yaml_payload(resolved)
    validate_cpu_execution_manifest_payload(payload, source_text=resolved.read_text(encoding="utf-8"))
    return CPUExecutionManifest(payload=payload, path=str(resolved), sha256=compute_sha256(resolved))


def load_yaml_payload(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"CPU execution manifest must be a YAML mapping: {path}")
    return payload


def validate_cpu_execution_manifest_payload(
    payload: dict[str, Any],
    *,
    source_text: str = "",
) -> None:
    validate_payload(payload, "cpu-execution-manifest-v0.schema.json")
    if payload.get("execution_enabled") is not True:
        raise ValueError("Stage 2F CPU execution manifests require execution_enabled=true.")
    if payload.get("execution_scope") not in ALLOWED_EXECUTION_SCOPES:
        raise ValueError(f"Unsupported execution_scope: {payload.get('execution_scope')}")
    for field in FALSE_FIELDS:
        if payload.get(field) is not False:
            raise ValueError(f"Stage 2F CPU execution manifests require {field}=false.")
    _validate_corpus_slice(payload)
    if _looks_like_raw_dump(source_text):
        raise ValueError("CPU execution manifest appears to include raw corpus data.")
    synthetic = payload.get("synthetic_corpus_record")
    if isinstance(synthetic, dict):
        validate_payload(synthetic, "synthetic-corpus-record-v0.schema.json")
        if synthetic.get("contains_liber_primus_unsolved_text") is not False:
            raise ValueError("Synthetic records must not include unsolved Liber Primus text.")


def _validate_corpus_slice(payload: dict[str, Any]) -> None:
    corpus_slice = payload.get("corpus_slice", {})
    if not isinstance(corpus_slice, dict):
        raise ValueError("corpus_slice must be a mapping.")
    slice_kind = corpus_slice.get("slice_kind")
    if slice_kind == "future_unsolved_page_candidate":
        raise ValueError("Stage 2F blocks future_unsolved_page_candidate execution.")
    if slice_kind == "page_candidate" and corpus_slice.get("solved_fixture_only") is not True:
        raise ValueError("Stage 2F blocks page_candidate execution unless solved_fixture_only=true.")
    scope = payload.get("execution_scope")
    if scope == "synthetic_only" and slice_kind != "synthetic":
        raise ValueError("synthetic_only execution requires a synthetic corpus slice.")
    if scope == "solved_fixture_only" and slice_kind != "solved_fixture_group":
        raise ValueError("solved_fixture_only execution requires a solved fixture group slice.")


def _looks_like_raw_dump(text: str) -> bool:
    return len(text) > 30000 or "data/raw/" in text or text.count("\n") > 1400

