"""Validation for Stage 4G cookie refresh outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.cookie_refresh.summary import load_summary
from libreprimus.history.source_records import resolve_repo_path


def validate_cookie_refresh_results(*, results_dir: Path, summary: Path) -> tuple[dict[str, int], list[str]]:
    """Validate generated Stage 4G result files and committed aggregate summary."""

    resolved_results = resolve_repo_path(results_dir)
    summary_payload = load_summary(resolve_repo_path(summary))
    errors: list[str] = []
    candidate_records = _read_jsonl(resolved_results / "candidate_records.jsonl")
    exact_matches = _read_jsonl(resolved_results / "exact_matches.jsonl")
    duplicates = _read_jsonl(resolved_results / "duplicate_candidates.jsonl")
    warnings = _read_jsonl(resolved_results / "warnings.jsonl")
    generated_summary = _read_json(resolved_results / "summary.json")

    for key in (
        "exact_match_only",
        "no_solve_claim",
    ):
        if summary_payload.get(key) is not True:
            errors.append(f"summary {key} must be true")
    for key in (
        "fuzzy_matching",
        "partial_matching",
        "hashcat_used",
        "cuda_used",
        "cloud_execution",
        "trusted_as_canonical",
        "generated_outputs_committed",
    ):
        if summary_payload.get(key) is not False:
            errors.append(f"summary {key} must be false")
    if summary_payload.get("candidates_after_dedup", 0) > summary_payload.get("candidate_count_upper_bound", -1):
        errors.append("candidate count exceeds cap")
    if summary_payload.get("comparison_count") != len(candidate_records):
        errors.append("summary comparison_count mismatch")
    if summary_payload.get("exact_match_count") != len(exact_matches):
        errors.append("summary exact_match_count mismatch")
    if generated_summary.get("comparison_count") != summary_payload.get("comparison_count"):
        errors.append("generated summary and committed summary disagree")

    declared_variants = set(summary_payload.get("byte_variants", []))
    declared_algorithms = set(summary_payload.get("algorithms_run", []))
    for record in candidate_records:
        _validate_candidate_record(record, declared_variants, declared_algorithms, errors)
    for record in exact_matches:
        if record.get("exact_match") is not True:
            errors.append(f"{record.get('candidate_id')}: exact match record is not exact")

    counts = {
        "candidate_records": len(candidate_records),
        "exact_matches": len(exact_matches),
        "duplicate_candidates": len(duplicates),
        "warnings": len(warnings),
        "target_cookie_count": int(summary_payload.get("target_cookie_count", 0)),
        "source_backed_base_string_count": int(summary_payload.get("source_backed_base_string_count", 0)),
        "candidates_after_dedup": int(summary_payload.get("candidates_after_dedup", 0)),
        "comparison_count": int(summary_payload.get("comparison_count", 0)),
    }
    return counts, errors


def _validate_candidate_record(
    record: dict[str, Any],
    declared_variants: set[str],
    declared_algorithms: set[str],
    errors: list[str],
) -> None:
    candidate_id = str(record.get("candidate_id", "<missing>"))
    if not record.get("source_basis"):
        errors.append(f"{candidate_id}: missing source_basis")
    if record.get("byte_variant") not in declared_variants:
        errors.append(f"{candidate_id}: undeclared byte variant")
    if record.get("algorithm") not in declared_algorithms:
        errors.append(f"{candidate_id}: undeclared algorithm")
    for key in ("no_solve_claim", "exact_match_only"):
        if record.get(key) is not True:
            errors.append(f"{candidate_id}: {key} must be true")
    for key in ("cuda_used", "cloud_execution", "trusted_as_canonical", "fuzzy_matching", "partial_matching", "hashcat_used", "broad_search"):
        if record.get(key) is not False:
            errors.append(f"{candidate_id}: {key} must be false")


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"missing generated summary: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON file must be a mapping: {path}")
    return payload


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise ValueError(f"missing generated JSONL: {path}")
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        if not isinstance(payload, dict):
            raise ValueError(f"JSONL record must be a mapping: {path}")
        records.append(payload)
    return records
