"""Validation for Stage 5Q Gematria expansion candidate mapping records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.benchmark_planning.export import read_json, read_yaml, resolve_repo_path
from libreprimus.gematria_expansion_candidate_mapping.export import read_record_set
from libreprimus.gematria_expansion_candidate_mapping.models import (
    BAD_TRUE_FLAGS,
    CANDIDATE_INVENTORY_PATH,
    CANDIDATE_INVENTORY_SCHEMA,
    EXPANSION_GATE_PATH,
    EXPANSION_GATE_SCHEMA,
    NATIVE_PARITY_PATH,
    NATIVE_PARITY_SCHEMA,
    OUTPUT_DIR,
    REQUIRED_TRUE_FLAGS,
    RESULT_STORE_PREFLIGHT_PATH,
    RESULT_STORE_PREFLIGHT_SCHEMA,
    SUMMARY_PATH,
    SUMMARY_REPORT,
    SUMMARY_SCHEMA,
    TOKEN_MAPPING_PATH,
    TOKEN_MAPPING_SCHEMA,
)


def validate_stage5q_results(
    *,
    candidate_inventory_path: Path = CANDIDATE_INVENTORY_PATH,
    token_mapping_path: Path = TOKEN_MAPPING_PATH,
    native_parity_path: Path = NATIVE_PARITY_PATH,
    result_store_preflight_path: Path = RESULT_STORE_PREFLIGHT_PATH,
    expansion_gate_path: Path = EXPANSION_GATE_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, Any], list[str]]:
    inventory = read_record_set(candidate_inventory_path)
    mappings = read_record_set(token_mapping_path)
    native = read_record_set(native_parity_path)
    preflight = read_record_set(result_store_preflight_path)
    gate = read_record_set(expansion_gate_path)
    summary = read_yaml(summary_path)
    generated_summary_path = resolve_repo_path(results_dir) / SUMMARY_REPORT
    generated_summary = read_json(generated_summary_path) if generated_summary_path.is_file() else summary
    errors: list[str] = []
    errors.extend(_validate_records(inventory, CANDIDATE_INVENTORY_SCHEMA, "candidate_inventory"))
    errors.extend(_validate_records(mappings, TOKEN_MAPPING_SCHEMA, "token_mapping"))
    errors.extend(_validate_records(native, NATIVE_PARITY_SCHEMA, "native_parity"))
    errors.extend(_validate_records(preflight, RESULT_STORE_PREFLIGHT_SCHEMA, "result_store_preflight"))
    errors.extend(_validate_records(gate, EXPANSION_GATE_SCHEMA, "expansion_gate"))
    errors.extend(_validate_one(summary, SUMMARY_SCHEMA, "summary"))
    errors.extend(_validate_one(generated_summary, SUMMARY_SCHEMA, "generated_summary"))
    if generated_summary != summary:
        errors.append("Committed Stage 5Q summary does not match generated summary.json")
    errors.extend(_semantic_errors([*inventory, *mappings, *native, *preflight, *gate, summary]))
    new_candidates = [record for record in inventory if record.get("candidate_status") == "candidate_for_mapping"]
    consumed_controls = [record for record in inventory if record.get("candidate_status") == "already_consumed_control"]
    mapped = [record for record in mappings if record.get("mapping_status") == "mapped"]
    prepared = [record for record in native if record.get("native_parity_status") == "prepared"]
    ready_preflight = [record for record in preflight if record.get("preflight_status") == "ready_for_future_result_store_integration"]
    if len(consumed_controls) != 5:
        errors.append("Stage 5Q must label the exact five Stage 5L/5M/5O buffers as consumed controls")
    if len(mapped) != len(new_candidates):
        errors.append("Stage 5Q mapped count must match candidate_for_mapping count")
    if len(prepared) != len(mapped):
        errors.append("Stage 5Q native parity prepared count must match mapped count")
    if len(ready_preflight) != len(mapped):
        errors.append("Stage 5Q ready result-store preflight count must match mapped count")
    if summary.get("new_candidate_count") != len(new_candidates):
        errors.append("Stage 5Q summary new_candidate_count mismatch")
    if summary.get("mapped_count") != len(mapped):
        errors.append("Stage 5Q summary mapped_count mismatch")
    if summary.get("native_parity_prepared_count") != len(prepared):
        errors.append("Stage 5Q summary native_parity_prepared_count mismatch")
    if summary.get("generated_body_publication_allowed") is not False:
        errors.append("Stage 5Q must keep generated_body_publication_allowed=false")
    if summary.get("method_status_upgrade_allowed") is not False:
        errors.append("Stage 5Q must keep method_status_upgrade_allowed=false")
    counts = {
        "candidate_inventory_records": len(inventory),
        "new_candidate_count": len(new_candidates),
        "already_consumed_control_records": len(consumed_controls),
        "mapped_count": len(mapped),
        "blocked_count": len(mappings) - len(mapped),
        "native_parity_prepared_count": len(prepared),
        "result_store_preflight_records": len(preflight),
        "stage4p_compatibility": str(summary.get("stage4p_compatibility", False)).lower(),
        "stage4i_compatibility": str(summary.get("stage4i_compatibility", False)).lower(),
        "stage5r_ready": str(summary.get("stage5r_ready", False)).lower(),
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


def _semantic_errors(records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for record in records:
        ident = str(record.get("record_type", "record"))
        if record.get("stage_id") not in (None, "stage-5q"):
            errors.append(f"{ident}: stage_id must be stage-5q")
        if record.get("new_cuda_kernels_added") not in (0, None):
            errors.append(f"{ident}: new_cuda_kernels_added must be 0")
        for key in BAD_TRUE_FLAGS:
            if record.get(key) is True:
                errors.append(f"{ident}: {key} must be false")
        for key in REQUIRED_TRUE_FLAGS:
            if record.get(key) is not True:
                errors.append(f"{ident}: {key} must be true")
        if record.get("mapping_status") == "mapped":
            if record.get("mapping_hash") is None:
                errors.append(f"{ident}: mapped token mappings require mapping_hash")
            values = record.get("token_values", [])
            mask = record.get("transformable_mask", [])
            if len(values) != len(mask):
                errors.append(f"{ident}: token_values and transformable_mask length mismatch")
            for value, transformable in zip(values, mask, strict=False):
                if transformable and (not isinstance(value, int) or value < 0 or value > 28):
                    errors.append(f"{ident}: transformable token value outside 0..28")
        if record.get("native_parity_status") == "prepared" and not record.get("output_token_hash"):
            errors.append(f"{ident}: prepared native parity records require output_token_hash")
        if record.get("preflight_status") == "ready_for_future_result_store_integration":
            if record.get("stage4p_compatibility") is not True or record.get("stage4i_compatibility") is not True:
                errors.append(f"{ident}: ready preflight requires Stage 4P and Stage 4I compatibility")
        if record.get("confidence_interpretation") not in (None, "triage_only"):
            errors.append(f"{ident}: confidence_interpretation must be triage_only")
    return errors
