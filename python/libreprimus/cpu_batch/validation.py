"""Validation for CPU batch manifests and generated results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.cpu_batch.models import (
    CPU_BATCH_CANDIDATE_SCHEMA,
    CPU_BATCH_ADAPTER_COVERAGE_SCHEMA,
    CPU_BATCH_ADAPTER_EXPANSION_SUMMARY_SCHEMA,
    CPU_BATCH_INPUT_SCHEMA,
    CPU_BATCH_MANIFEST_SCHEMA,
    CPU_BATCH_PARITY_EXPECTATION_SCHEMA,
    CPU_BATCH_RESULT_SCHEMA,
    CPU_BATCH_SUMMARY_SCHEMA,
    CPU_BATCH_SCORING_COMPATIBILITY_SCHEMA,
)
from libreprimus.history.source_records import resolve_repo_path


def validate_manifest_path(path: Path) -> list[str]:
    """Validate a CPU batch manifest file."""

    import yaml

    payload = yaml.safe_load(resolve_repo_path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return [f"manifest must be a mapping: {path}"]
    return validate_manifest_payload(payload)


def validate_manifest_payload(payload: dict[str, Any]) -> list[str]:
    """Validate manifest JSON-schema and policy-level constraints."""

    errors = _validate_with_refs(payload, CPU_BATCH_MANIFEST_SCHEMA)
    candidates = payload.get("transform_candidates", [])
    cap = int(payload.get("candidate_count_upper_bound", -1))
    if isinstance(candidates, list) and len(candidates) > cap:
        errors.append("candidate_count_upper_bound exceeded")
    for key, expected in (
        ("cpu_only", True),
        ("cuda_used", False),
        ("cuda_required", False),
        ("no_solve_claim", True),
        ("canonical_corpus_active", False),
        ("page_boundaries_final", False),
        ("generated_outputs_committed", False),
    ):
        if payload.get(key) is not expected:
            errors.append(f"{key} must be {str(expected).lower()}")
    return errors


def validate_results_dir(results_dir: Path) -> tuple[dict[str, int], list[str]]:
    """Validate generated CPU batch result files."""

    resolved = resolve_repo_path(results_dir)
    errors: list[str] = []
    records = _read_jsonl(resolved / "result_records.jsonl")
    summary = _read_json(resolved / "summary.json")
    errors.extend(_validate_with_refs(summary, CPU_BATCH_SUMMARY_SCHEMA))
    if summary.get("result_record_count") != len(records):
        errors.append("summary result_record_count mismatch")
    for record in records:
        errors.extend(_validate_with_refs(record, CPU_BATCH_RESULT_SCHEMA))
        if record.get("cuda_used") is not False:
            errors.append(f"{record.get('candidate_id')}: cuda_used must be false")
        if record.get("no_solve_claim") is not True:
            errors.append(f"{record.get('candidate_id')}: no_solve_claim must be true")
    coverage_path = resolved / "adapter_coverage.json"
    coverage = _read_json(coverage_path) if coverage_path.is_file() else {}
    counts = {
        "result_records": len(records),
        "executed_candidates": int(summary.get("executed_candidate_count", 0)),
        "adapter_missing": int(summary.get("adapter_missing_count", 0)),
        "scoring_available": int(summary.get("scoring_available_count", 0)),
        "scoring_unavailable": int(summary.get("scoring_unavailable_count", 0)),
        "adapter_coverage_supported": int(coverage.get("supported_adapter_count", 0)),
        "adapter_coverage_missing": int(coverage.get("missing_adapter_count", 0)),
    }
    return counts, errors


def validate_stage4o_results(results_dir: Path, summary_path: Path) -> tuple[dict[str, int], list[str]]:
    """Validate Stage 4O generated records and committed summary."""

    resolved = resolve_repo_path(results_dir)
    errors: list[str] = []
    records = _read_jsonl(resolved / "result_records.jsonl")
    adapter_coverage = _read_json(resolved / "adapter_coverage.json")
    parity_records = _read_jsonl(resolved / "parity_expectations.jsonl")
    scoring = _read_json(resolved / "scoring_compatibility.json")
    summary = _read_yaml(resolve_repo_path(summary_path))

    errors.extend(_validate_with_refs(adapter_coverage, CPU_BATCH_ADAPTER_COVERAGE_SCHEMA))
    errors.extend(_validate_with_refs(scoring, CPU_BATCH_SCORING_COMPATIBILITY_SCHEMA))
    errors.extend(_validate_with_refs(summary, CPU_BATCH_ADAPTER_EXPANSION_SUMMARY_SCHEMA))
    for record in records:
        errors.extend(_validate_with_refs(record, CPU_BATCH_RESULT_SCHEMA))
        if record.get("cuda_used") is not False:
            errors.append(f"{record.get('candidate_id')}: cuda_used must be false")
        if record.get("no_solve_claim") is not True:
            errors.append(f"{record.get('candidate_id')}: no_solve_claim must be true")
    for record in parity_records:
        errors.extend(_validate_with_refs(record, CPU_BATCH_PARITY_EXPECTATION_SCHEMA))
        if record.get("cuda_used") is not False:
            errors.append(f"{record.get('candidate_id')}: parity cuda_used must be false")
        if record.get("no_solve_claim") is not True:
            errors.append(f"{record.get('candidate_id')}: parity no_solve_claim must be true")
    if summary.get("result_records") != len(records):
        errors.append("Stage 4O summary result_records mismatch")
    if summary.get("parity_expectations_written") != len(parity_records):
        errors.append("Stage 4O summary parity_expectations_written mismatch")
    if scoring.get("record_count") != len(records):
        errors.append("Stage 4O scoring compatibility record_count mismatch")
    counts = {
        "result_records": len(records),
        "executed_candidates": int(summary.get("candidates_executed", 0)),
        "parity_expectations": len(parity_records),
        "adapter_supported": int(adapter_coverage.get("supported_adapter_count", 0)),
        "adapter_missing_or_deferred": int(adapter_coverage.get("missing_or_deferred_adapter_count", 0)),
        "scoring_compatible": int(scoring.get("scoring_compatible_count", 0)),
        "scoring_unavailable": int(scoring.get("scoring_unavailable_count", 0)),
    }
    return counts, errors


def _validate_with_refs(instance: dict[str, Any], schema_path: Path) -> list[str]:
    schema = json.loads(resolve_repo_path(schema_path).read_text(encoding="utf-8"))
    if schema_path == CPU_BATCH_MANIFEST_SCHEMA:
        schema = dict(schema)
        properties = dict(schema["properties"])
        input_streams = dict(properties["input_streams"])
        input_streams["items"] = {}
        transform_candidates = dict(properties["transform_candidates"])
        transform_candidates["items"] = {}
        properties["input_streams"] = input_streams
        properties["transform_candidates"] = transform_candidates
        schema["properties"] = properties
    validator = Draft202012Validator(schema)
    messages: list[str] = []
    for error in validator.iter_errors(instance):
        path = ".".join(str(part) for part in error.path)
        messages.append(f"{path}: {error.message}" if path else error.message)
    if schema_path == CPU_BATCH_MANIFEST_SCHEMA:
        for index, stream in enumerate(instance.get("input_streams", [])):
            if isinstance(stream, dict):
                for error in _validate_with_refs(stream, CPU_BATCH_INPUT_SCHEMA):
                    messages.append(f"input_streams.{index}: {error}")
        for index, candidate in enumerate(instance.get("transform_candidates", [])):
            if isinstance(candidate, dict):
                for error in _validate_with_refs(candidate, CPU_BATCH_CANDIDATE_SCHEMA):
                    messages.append(f"transform_candidates.{index}: {error}")
    return messages


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"missing JSON file: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON file must be a mapping: {path}")
    return payload


def _read_yaml(path: Path) -> dict[str, Any]:
    import yaml

    if not path.is_file():
        raise ValueError(f"missing YAML file: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"YAML file must be a mapping: {path}")
    return payload


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise ValueError(f"missing JSONL file: {path}")
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        if not isinstance(payload, dict):
            raise ValueError(f"JSONL line must be a mapping: {path}")
        records.append(payload)
    return records
