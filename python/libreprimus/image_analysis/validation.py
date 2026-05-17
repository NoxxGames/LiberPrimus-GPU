"""Validation for generated deterministic image-analysis records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.image_analysis.export import read_jsonl
from libreprimus.image_analysis.thresholds import DEFAULT_THRESHOLDS
from libreprimus.paths import repo_root

RESULT_FILES = {
    "analysis": "image_analysis_records.jsonl",
    "thresholds": "threshold_summary_records.jsonl",
    "symmetry": "symmetry_records.jsonl",
    "bitplanes": "bitplane_summary_records.jsonl",
    "components": "component_summary_records.jsonl",
    "features": "visual_feature_candidates.jsonl",
    "summary": "summary.json",
}

SCHEMA_FILES = {
    "analysis": repo_root() / "schemas/visual/image-analysis-record-v0.schema.json",
    "thresholds": repo_root() / "schemas/visual/image-threshold-summary-v0.schema.json",
    "symmetry": repo_root() / "schemas/visual/image-symmetry-record-v0.schema.json",
    "bitplanes": repo_root() / "schemas/visual/image-bitplane-summary-v0.schema.json",
    "components": repo_root() / "schemas/visual/image-component-summary-v0.schema.json",
    "features": repo_root() / "schemas/visual/visual-feature-candidate-v0.schema.json",
    "summary": repo_root() / "schemas/visual/image-analysis-run-summary-v0.schema.json",
}


def validate_results(results_dir: Path, *, allow_missing: bool = False) -> tuple[dict[str, int], list[str]]:
    resolved = _resolve(results_dir)
    if not resolved.exists():
        if allow_missing:
            return {"image_count": 0}, []
        return {"image_count": 0}, [f"results directory missing: {resolved}"]
    if allow_missing and not (resolved / "summary.json").is_file():
        return {"image_count": 0}, []

    errors: list[str] = []
    counts: dict[str, int] = {}
    for key, filename in RESULT_FILES.items():
        path = resolved / filename
        if key == "summary":
            if not path.is_file():
                errors.append(f"missing summary: {path}")
                continue
            payload = json.loads(path.read_text(encoding="utf-8"))
            _validate_schema(key, payload, errors)
            _validate_flags(payload, errors)
            counts["image_count"] = int(payload.get("image_count", 0))
            counts["feature_candidate_count"] = int(payload.get("feature_candidate_count", 0))
            continue
        if not path.is_file():
            errors.append(f"missing records: {path}")
            continue
        records = read_jsonl(path)
        counts[f"{key}_record_count"] = len(records)
        for record in records:
            _validate_schema(key, record, errors)
            _validate_flags(record, errors)
            if key == "features" and record.get("usable_as_experiment_seed") is not False:
                errors.append(f"{record.get('feature_id', '<unknown>')}: feature must not be an experiment seed")
            if key in {"thresholds", "components"} and record.get("threshold") not in DEFAULT_THRESHOLDS:
                errors.append(f"{record.get('image_id', '<unknown>')}: invalid threshold {record.get('threshold')}")
    return counts, errors


def _validate_schema(key: str, record: dict[str, Any], errors: list[str]) -> None:
    schema = json.loads(SCHEMA_FILES[key].read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    for error in validator.iter_errors(record):
        errors.append(f"{key}: {error.message}")


def _validate_flags(record: dict[str, Any], errors: list[str]) -> None:
    record_id = record.get("image_id") or record.get("run_id") or record.get("feature_id") or "<unknown>"
    if record.get("trusted_as_canonical") is not False:
        errors.append(f"{record_id}: trusted_as_canonical must be false")
    if record.get("solve_claim") is not False:
        errors.append(f"{record_id}: solve_claim must be false")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path
