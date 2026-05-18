"""Validation for Stage 3P generated image transform results."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.image_transforms.export import read_json, read_jsonl
from libreprimus.paths import repo_root

EXPECTED_FILES = [
    "transform_records.jsonl",
    "transform_metric_records.jsonl",
    "visual_transform_candidates.jsonl",
    "contact_sheet_manifest.jsonl",
    "summary.json",
]


def validate_results(results_dir: Path, *, allow_missing: bool = False) -> tuple[dict[str, int], list[str]]:
    """Validate generated Stage 3P output structure and safety flags."""
    resolved = results_dir if results_dir.is_absolute() else repo_root() / results_dir
    if not resolved.exists():
        if allow_missing:
            return {
                "transform_record_count": 0,
                "metric_record_count": 0,
                "candidate_count": 0,
                "contact_sheet_count": 0,
            }, []
        return {}, [f"results_dir_missing={resolved}"]

    errors: list[str] = []
    if allow_missing and not any((resolved / file_name).is_file() for file_name in EXPECTED_FILES):
        return {
            "transform_record_count": 0,
            "metric_record_count": 0,
            "candidate_count": 0,
            "contact_sheet_count": 0,
            "review_index_present": 0,
        }, []
    for file_name in EXPECTED_FILES:
        if not (resolved / file_name).is_file():
            errors.append(f"missing_output={file_name}")

    transform_records = read_jsonl(resolved / "transform_records.jsonl")
    metric_records = read_jsonl(resolved / "transform_metric_records.jsonl")
    candidate_records = read_jsonl(resolved / "visual_transform_candidates.jsonl")
    contact_records = read_jsonl(resolved / "contact_sheet_manifest.jsonl")
    summary = read_json(resolved / "summary.json") if (resolved / "summary.json").is_file() else {}

    for record in [*transform_records, *metric_records, *candidate_records, *contact_records, summary]:
        _validate_false_flags(record, errors)
        if str(record.get("record_type", "")).startswith("visual_transform"):
            if record.get("usable_as_experiment_seed") is not False:
                errors.append(f"{record.get('record_type')}: usable_as_experiment_seed must be false")
    for record in transform_records:
        output_path = repo_root() / str(record.get("output_relative_path", ""))
        if not output_path.is_file():
            errors.append(f"missing_derived_output={record.get('output_relative_path')}")
    counts = {
        "transform_record_count": len(transform_records),
        "metric_record_count": len(metric_records),
        "candidate_count": len(candidate_records),
        "contact_sheet_count": len(contact_records),
        "review_index_present": int((resolved / "review_index.html").is_file()),
    }
    return counts, errors


def _validate_false_flags(record: dict[str, Any], errors: list[str]) -> None:
    if not record:
        return
    record_type = record.get("record_type", "<unknown>")
    if record.get("trusted_as_canonical") is not False:
        errors.append(f"{record_type}: trusted_as_canonical must be false")
    if record.get("solve_claim") is not False:
        errors.append(f"{record_type}: solve_claim must be false")
