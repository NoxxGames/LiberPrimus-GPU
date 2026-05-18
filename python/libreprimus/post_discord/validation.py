"""Validation helpers for Stage 3S post-Discord outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.paths import repo_root
from libreprimus.post_discord.export import read_json, resolve_path
from libreprimus.post_discord.models import EXPERIMENT_ID
from libreprimus.post_discord.onion7_seed_pack import load_onion7_manifest


def validate_manifest(path: Path) -> tuple[dict[str, Any], list[str]]:
    """Validate the EXP-3R-003 manifest."""
    errors: list[str] = []
    try:
        manifest = load_onion7_manifest(path)
    except (OSError, ValueError) as exc:
        return {}, [str(exc)]
    schema = _read_schema("schemas/experiments/post-discord-experiment-manifest-v0.schema.json")
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(manifest.payload), key=str):
        errors.append(error.message)
    if manifest.experiment_id != EXPERIMENT_ID:
        errors.append(f"expected {EXPERIMENT_ID}")
    if manifest.expected_candidate_count > manifest.candidate_count_cap:
        errors.append("candidate count exceeds cap")
    return {
        "experiment_id": manifest.experiment_id,
        "candidate_count_cap": manifest.candidate_count_cap,
        "expected_candidate_count": manifest.expected_candidate_count,
        "value_spaces": manifest.value_spaces,
        "routes": manifest.routes,
        "directions": manifest.directions,
        "reset_modes": manifest.reset_modes,
    }, errors


def validate_results(results_dir: Path, *, allow_missing: bool = False) -> tuple[dict[str, Any], list[str]]:
    """Validate generated Stage 3S outputs if present."""
    resolved = resolve_path(results_dir)
    summary_path = resolved / "summary.json"
    if not summary_path.is_file():
        if allow_missing:
            return {"summary_present": False}, []
        return {}, [f"missing Stage 3S summary: {summary_path}"]
    errors: list[str] = []
    summary = read_json(summary_path)
    if summary.get("queue_item_id") != EXPERIMENT_ID:
        errors.append("summary queue_item_id must be EXP-3R-003")
    for field, expected in {
        "generated_outputs_ignored": True,
        "search_performed": True,
        "scoring_used": True,
        "cuda_used": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "solve_claim": False,
        "trusted_as_canonical": False,
    }.items():
        if summary.get(field) is not expected:
            errors.append(f"summary {field} must be {str(expected).lower()}")
    expected = int(summary.get("expected_candidate_count") or 0)
    executed = int(summary.get("executed_candidate_count") or 0)
    deferred = int(summary.get("deferred_candidate_count") or 0)
    if expected and executed + deferred != expected:
        errors.append("executed plus deferred candidate count must equal expected")
    for name in ["candidate_records.jsonl", "top_candidates.jsonl"]:
        path = resolved / name
        if not path.is_file():
            errors.append(f"missing generated output: {path}")
    return summary, errors


def _read_schema(relative: str) -> dict[str, Any]:
    return json.loads((repo_root() / relative).read_text(encoding="utf-8"))
