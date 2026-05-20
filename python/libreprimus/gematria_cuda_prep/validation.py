"""Validation for Stage 5I Gematria CUDA preparation records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.benchmark_planning.export import read_json, read_yaml, resolve_repo_path
from libreprimus.gematria_cuda_prep.export import read_record_set
from libreprimus.gematria_cuda_prep.models import (
    ABI_PLAN_PATH,
    ABI_PLAN_SCHEMA,
    BAD_TRUE_FLAGS,
    CHECKLIST_PATH,
    CHECKLIST_SCHEMA,
    NATIVE_FIXTURE_HASH,
    OUTPUT_DIR,
    PREPARATION_PATH,
    PREPARATION_SCHEMA,
    REQUIRED_TRUE_FLAGS,
    SOURCE_CONTRACT_ID,
    STAGE5F_HASH,
    SUMMARY_JSON,
    SUMMARY_PATH,
    SUMMARY_SCHEMA,
    TARGET_FUTURE_KERNEL_NAME,
    TOKEN_DOMAIN,
    VALIDATION_VECTOR_SCHEMA,
    VALIDATION_VECTORS_PATH,
)


def validate_stage5i_results(
    *,
    preparation_path: Path = PREPARATION_PATH,
    abi_plan_path: Path = ABI_PLAN_PATH,
    validation_vectors_path: Path = VALIDATION_VECTORS_PATH,
    implementation_checklist_path: Path = CHECKLIST_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, Any], list[str]]:
    """Validate committed and generated Stage 5I records."""

    preparations = read_record_set(preparation_path)
    abi_plans = read_record_set(abi_plan_path)
    vectors = read_record_set(validation_vectors_path)
    checklists = read_record_set(implementation_checklist_path)
    summary = read_yaml(summary_path)
    generated_summary_path = resolve_repo_path(results_dir) / SUMMARY_JSON
    generated_summary = read_json(generated_summary_path) if generated_summary_path.is_file() else summary
    errors: list[str] = []
    errors.extend(_validate_records(preparations, PREPARATION_SCHEMA, "preparation"))
    errors.extend(_validate_records(abi_plans, ABI_PLAN_SCHEMA, "abi_plan"))
    errors.extend(_validate_records(vectors, VALIDATION_VECTOR_SCHEMA, "validation_vector"))
    errors.extend(_validate_records(checklists, CHECKLIST_SCHEMA, "checklist"))
    errors.extend(_validate_one(summary, SUMMARY_SCHEMA, "summary"))
    errors.extend(_validate_one(generated_summary, SUMMARY_SCHEMA, "generated_summary"))
    if generated_summary != summary:
        errors.append("Committed Stage 5I summary does not match generated summary.json")
    records = [*preparations, *abi_plans, *vectors, *checklists, summary]
    errors.extend(_semantic_errors(records))
    vector = vectors[0] if vectors else {}
    summary_counts = {
        "preparation_id": summary.get("preparation_id"),
        "source_contract_id": summary.get("source_contract_id"),
        "target_future_kernel_name": summary.get("target_future_kernel_name"),
        "token_domain": summary.get("token_domain"),
        "arithmetic_direction": summary.get("arithmetic_direction"),
        "separator_policy": summary.get("separator_policy"),
        "abi_plan_records": len(abi_plans),
        "validation_vector_records": len(vectors),
        "implementation_checklist_records": len(checklists),
        "native_fixture_id": summary.get("native_fixture_id"),
        "native_fixture_hash": summary.get("native_fixture_hash"),
        "stage5f_hash_is_gematria_fixture_hash": str(vector.get("stage5f_hash_is_gematria_fixture_hash")).lower(),
        "stage5j_ready_for_synthetic_implementation": str(summary.get("stage5j_ready_for_synthetic_implementation")).lower(),
        "cuda_source_modified": str(summary.get("cuda_source_modified")).lower(),
        "new_cuda_kernels_added": int(summary.get("new_cuda_kernels_added", -1)),
        "cuda_execution_performed": str(summary.get("cuda_execution_performed")).lower(),
        "solved_fixture_cuda_execution_allowed": str(summary.get("solved_fixture_cuda_execution_allowed")).lower(),
        "production_gematria_mod29_cuda_ready": str(summary.get("production_gematria_mod29_cuda_ready")).lower(),
        "gpu_benchmark_performed": int(bool(summary.get("gpu_benchmark_performed"))),
        "performance_or_speedup_claim": int(bool(summary.get("performance_claim") or summary.get("speedup_claim"))),
        "real_liber_primus_data_used": str(summary.get("real_liber_primus_data_used")).lower(),
    }
    return summary_counts, errors


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


def _semantic_errors(records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for record in records:
        ident = str(record.get("record_type", "record"))
        if record.get("source_contract_id") != SOURCE_CONTRACT_ID:
            errors.append(f"{ident}: source_contract_id must be {SOURCE_CONTRACT_ID}")
        if record.get("target_future_kernel_name") != TARGET_FUTURE_KERNEL_NAME:
            errors.append(f"{ident}: target_future_kernel_name must be {TARGET_FUTURE_KERNEL_NAME}")
        if record.get("token_domain") != TOKEN_DOMAIN:
            errors.append(f"{ident}: token_domain must be {TOKEN_DOMAIN}")
        if record.get("native_fixture_hash") != NATIVE_FIXTURE_HASH:
            errors.append(f"{ident}: native_fixture_hash must be Stage 5H hash")
        if record.get("expected_fixture_hash") not in {None, NATIVE_FIXTURE_HASH}:
            errors.append(f"{ident}: expected_fixture_hash must be Stage 5H hash")
        if record.get("stage5f_hash_is_gematria_fixture_hash") is True:
            errors.append(f"{ident}: Stage 5F hash must not be treated as the Gematria fixture hash")
        if record.get("expected_fixture_hash") == STAGE5F_HASH:
            errors.append(f"{ident}: Gematria fixture hash must differ from Stage 5F uppercase Latin hash")
        if record.get("new_cuda_kernels_added") not in {0, None}:
            errors.append(f"{ident}: new_cuda_kernels_added must be 0")
        for key in BAD_TRUE_FLAGS:
            if record.get(key) is True:
                errors.append(f"{ident}: {key} must be false")
        for key in REQUIRED_TRUE_FLAGS:
            if record.get(key) is not True:
                errors.append(f"{ident}: {key} must be true")
        if record.get("record_type") == "gematria_cuda_abi_plan_record":
            errors.extend(_abi_errors(record, ident))
        if record.get("record_type") == "gematria_cuda_validation_vector_record":
            errors.extend(_vector_errors(record, ident))
    return errors


def _abi_errors(record: dict[str, Any], ident: str) -> list[str]:
    errors: list[str] = []
    if record.get("c_compatible_kernel_boundary") is not True:
        errors.append(f"{ident}: c_compatible_kernel_boundary must be true")
    for key in (
        "stl_in_device_path_allowed",
        "exceptions_in_device_path_allowed",
        "dynamic_allocation_in_device_path_allowed",
        "strings_cross_kernel_boundary",
        "host_ownership_types_cross_kernel_boundary",
    ):
        if record.get(key) is not False:
            errors.append(f"{ident}: {key} must be false")
    buffer_layout = record.get("buffer_layout", {})
    if not isinstance(buffer_layout, dict):
        errors.append(f"{ident}: buffer_layout must be a mapping")
        return errors
    for key in ("token_values", "transformable_mask", "shifts", "output_token_values", "token_count", "candidate_count"):
        if key not in buffer_layout:
            errors.append(f"{ident}: missing ABI buffer {key}")
    return errors


def _vector_errors(record: dict[str, Any], ident: str) -> list[str]:
    errors: list[str] = []
    if record.get("input_token_values") != [0, 1, 0, 28, 13, 0, 5]:
        errors.append(f"{ident}: input_token_values do not match Stage 5H fixture buffer")
    if record.get("transformable_mask") != [1, 1, 0, 1, 1, 0, 1]:
        errors.append(f"{ident}: transformable_mask must preserve separator positions")
    if record.get("separator_positions") != [2, 5]:
        errors.append(f"{ident}: separator_positions must be [2, 5]")
    return errors
