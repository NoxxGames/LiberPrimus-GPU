"""Validation for Stage 5L solved-fixture-safe Gematria mapping records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.benchmark_planning.export import read_json, read_yaml, resolve_repo_path
from libreprimus.gematria_solved_fixture_mapping.export import read_record_set
from libreprimus.gematria_solved_fixture_mapping.models import (
    ALLOWED_CONFIDENCE_LABELS,
    BAD_TRUE_FLAGS,
    HASH_ALGORITHM,
    NATIVE_PARITY_PATH,
    NATIVE_PARITY_SCHEMA,
    OUTPUT_DIR,
    OUTPUT_HASH_CONTRACT_PATH,
    OUTPUT_HASH_CONTRACT_SCHEMA,
    OUTPUT_ORDERING,
    REQUIRED_TRUE_FLAGS,
    SCORE_SUMMARY_CONTRACT,
    SCORE_SUMMARY_SHAPE_PATH,
    SCORE_SUMMARY_SHAPE_SCHEMA,
    SUMMARY_JSON,
    SUMMARY_PATH,
    SUMMARY_SCHEMA,
    TOKEN_DOMAIN,
    TOKEN_DOMAIN_MAX,
    TOKEN_DOMAIN_MIN,
    TOKEN_MAPPING_PATH,
    TOKEN_MAPPING_SCHEMA,
)


def validate_stage5l_results(
    *,
    token_mapping_path: Path = TOKEN_MAPPING_PATH,
    native_parity_path: Path = NATIVE_PARITY_PATH,
    output_hash_contract_path: Path = OUTPUT_HASH_CONTRACT_PATH,
    score_summary_shape_path: Path = SCORE_SUMMARY_SHAPE_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, Any], list[str]]:
    mapping_records = read_record_set(token_mapping_path)
    native_records = read_record_set(native_parity_path)
    hash_records = read_record_set(output_hash_contract_path)
    score_records = read_record_set(score_summary_shape_path)
    summary = read_yaml(summary_path)
    generated_summary_path = resolve_repo_path(results_dir) / SUMMARY_JSON
    generated_summary = read_json(generated_summary_path) if generated_summary_path.is_file() else summary
    errors: list[str] = []
    errors.extend(_validate_records(mapping_records, TOKEN_MAPPING_SCHEMA, "token_mapping"))
    errors.extend(_validate_records(native_records, NATIVE_PARITY_SCHEMA, "native_parity"))
    errors.extend(_validate_records(hash_records, OUTPUT_HASH_CONTRACT_SCHEMA, "output_hash_contract"))
    errors.extend(_validate_records(score_records, SCORE_SUMMARY_SHAPE_SCHEMA, "score_summary_shape"))
    errors.extend(_validate_one(summary, SUMMARY_SCHEMA, "summary"))
    errors.extend(_validate_one(generated_summary, SUMMARY_SCHEMA, "generated_summary"))
    if generated_summary != summary:
        errors.append("Committed Stage 5L summary does not match generated summary.json")
    errors.extend(_semantic_errors(mapping_records, native_records, hash_records, score_records, summary))
    counts = {
        "token_mapping_records": len(mapping_records),
        "mapped_count": sum(1 for record in mapping_records if record.get("mapping_status") == "mapped"),
        "blocked_count": sum(1 for record in mapping_records if record.get("mapping_status") != "mapped"),
        "native_parity_fixture_records": len(native_records),
        "native_parity_prepared_count": sum(
            1 for record in native_records if record.get("native_parity_status") == "prepared"
        ),
        "output_hash_contract_records": len(hash_records),
        "score_summary_shape_records": len(score_records),
        "blocker_count_before": int(summary.get("blocker_count_before", -1)),
        "blocker_count_after": int(summary.get("blocker_count_after", -1)),
        "readiness_status_counts": summary.get("readiness_status_counts", {}),
        "selected_next_stage": summary.get("selected_next_stage"),
    }
    return counts, errors


def _validate_records(records: list[dict[str, Any]], schema_path: Path, label: str) -> list[str]:
    errors: list[str] = []
    for index, record in enumerate(records):
        errors.extend(_validate_one(record, schema_path, f"{label}[{index}]"))
    return errors


def _validate_one(record: dict[str, Any], schema_path: Path, label: str) -> list[str]:
    schema = json.loads(resolve_repo_path(schema_path).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    return [
        f"{label}.{'.'.join(str(part) for part in error.path)}: {error.message}"
        if error.path
        else f"{label}: {error.message}"
        for error in validator.iter_errors(record)
    ]


def _semantic_errors(
    mapping_records: list[dict[str, Any]],
    native_records: list[dict[str, Any]],
    hash_records: list[dict[str, Any]],
    score_records: list[dict[str, Any]],
    summary: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    all_records = [*mapping_records, *native_records, *hash_records, *score_records, summary]
    for record in all_records:
        ident = str(record.get("record_type", "record"))
        for key in BAD_TRUE_FLAGS:
            if record.get(key) is True:
                errors.append(f"{ident}: {key} must be false")
        for key in REQUIRED_TRUE_FLAGS:
            if record.get(key) is not True:
                errors.append(f"{ident}: {key} must be true")
        if record.get("new_cuda_kernels_added") not in {0, None}:
            errors.append(f"{ident}: new_cuda_kernels_added must be 0")
    for record in mapping_records:
        if record.get("token_domain") != TOKEN_DOMAIN:
            errors.append(f"{record['mapping_id']}: token_domain must be {TOKEN_DOMAIN}")
        token_values = record.get("token_values", [])
        mask = record.get("transformable_mask", [])
        if len(mask) != int(record.get("token_count", -1)):
            errors.append(f"{record['mapping_id']}: transformable_mask length must equal token_count")
        for value, transformable in zip(token_values, mask, strict=False):
            if transformable and (not isinstance(value, int) or not TOKEN_DOMAIN_MIN <= value <= TOKEN_DOMAIN_MAX):
                errors.append(f"{record['mapping_id']}: transformable token values must be 0..28")
        if record.get("mapping_status") == "mapped" and record.get("source_backed_token_values") is not True:
            errors.append(f"{record['mapping_id']}: mapped records require source-backed token values")
        if record.get("separator_metadata_preserved") is not True:
            errors.append(f"{record['mapping_id']}: separator metadata must be preserved")
        if record.get("token_kind_metadata_preserved") is not True:
            errors.append(f"{record['mapping_id']}: token kind metadata must be preserved")
    for record in native_records:
        if record.get("native_parity_status") == "prepared" and not record.get("output_token_hash"):
            errors.append(f"{record['native_parity_record_id']}: prepared records require output_token_hash")
        if record.get("native_parity_status") == "blocked" and not record.get("blockers"):
            errors.append(f"{record['native_parity_record_id']}: blocked records require blockers")
    for record in hash_records:
        if record.get("candidate_ordering_required") != OUTPUT_ORDERING:
            errors.append("output hash contract requires candidate-major ordering")
        if record.get("hash_algorithm") != HASH_ALGORITHM:
            errors.append(f"output hash contract requires {HASH_ALGORITHM}")
    for record in score_records:
        if record.get("score_summary_contract") != SCORE_SUMMARY_CONTRACT:
            errors.append("score summary shape must use Stage 4I contract")
        if record.get("score_interpretation") != "triage_only":
            errors.append("score summary interpretation must be triage_only")
        labels = set(record.get("allowed_confidence_labels", []))
        if not labels.issubset(set(ALLOWED_CONFIDENCE_LABELS)):
            errors.append("score summary shape contains labels outside Stage 4I vocabulary")
    if summary.get("token_mapping_records") != len(mapping_records):
        errors.append("summary token_mapping_records count mismatch")
    if summary.get("native_parity_fixture_records") != len(native_records):
        errors.append("summary native_parity_fixture_records count mismatch")
    if summary.get("solved_fixture_cuda_execution_allowed") is not False:
        errors.append("summary must keep solved_fixture_cuda_execution_allowed=false")
    return errors
