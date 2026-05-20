"""Validation for Stage 5E CUDA kernel contract records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.benchmark_planning.export import read_json, read_yaml, resolve_repo_path
from libreprimus.cuda_kernel_contract.loaders import load_records
from libreprimus.cuda_kernel_contract.models import (
    ADAPTER_SELECTION_PATH,
    ADAPTER_SELECTION_SCHEMA,
    COMMON_GUARDRAILS,
    CONTRACT_PATH,
    CONTRACT_SCHEMA,
    NATIVE_PARITY_PATH,
    NATIVE_PARITY_SCHEMA,
    OUTPUT_DIR,
    READINESS_PATH,
    READINESS_SCHEMA,
    SUMMARY_PATH,
    SUMMARY_REPORT,
    SUMMARY_SCHEMA,
)


def validate_stage5e_results(
    *,
    contract_path: Path = CONTRACT_PATH,
    adapter_selection_path: Path = ADAPTER_SELECTION_PATH,
    native_parity_path: Path = NATIVE_PARITY_PATH,
    readiness_path: Path = READINESS_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, Any], list[str]]:
    contract = load_records(contract_path)
    adapter = load_records(adapter_selection_path)
    native = load_records(native_parity_path)
    readiness = load_records(readiness_path)
    summary = read_yaml(summary_path)
    generated_summary_path = resolve_repo_path(results_dir) / SUMMARY_REPORT
    generated_summary = read_json(generated_summary_path) if generated_summary_path.is_file() else summary
    errors: list[str] = []
    errors.extend(_validate_records(contract, CONTRACT_SCHEMA, "contract"))
    errors.extend(_validate_records(adapter, ADAPTER_SELECTION_SCHEMA, "adapter"))
    errors.extend(_validate_records(native, NATIVE_PARITY_SCHEMA, "native_parity"))
    errors.extend(_validate_records(readiness, READINESS_SCHEMA, "readiness"))
    errors.extend(_validate_one(summary, SUMMARY_SCHEMA, "summary"))
    errors.extend(_validate_one(generated_summary, SUMMARY_SCHEMA, "generated_summary"))
    if generated_summary != summary:
        errors.append("Committed Stage 5E summary does not match generated summary.json")
    errors.extend(_semantic_errors(contract, adapter, native, readiness, summary))
    counts = {
        "contract_records": len(contract),
        "adapter_selection_records": len(adapter),
        "native_parity_adapter_records": len(native),
        "implementation_readiness_records": len(readiness),
        "selected_kernel_id": summary.get("selected_kernel_id"),
        "selected_transform_family": summary.get("selected_transform_family"),
        "selected_adapter_family": summary.get("selected_adapter_family"),
        "alternate_candidate_count": int(summary.get("alternate_candidate_count", 0)),
        "blocked_rejected_candidate_count": int(summary.get("blocked_rejected_candidate_count", 0)),
        "native_parity_mapped": str(summary.get("native_parity_mapped")).lower(),
        "implementation_readiness_status": summary.get("implementation_readiness_status"),
        "cuda_kernel_added": int(bool(summary.get("cuda_kernel_added"))),
        "cuda_source_modified": int(bool(summary.get("cuda_source_modified"))),
        "cuda_transform_executed": int(bool(summary.get("cuda_transform_executed"))),
        "gpu_benchmark_performed": int(bool(summary.get("gpu_benchmark_performed"))),
        "performance_or_speedup_claim": int(bool(summary.get("performance_claim") or summary.get("speedup_claim"))),
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
    contract: list[dict[str, Any]],
    adapter: list[dict[str, Any]],
    native: list[dict[str, Any]],
    readiness: list[dict[str, Any]],
    summary: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    if len(contract) != 1:
        errors.append("Stage 5E must select exactly one first kernel contract")
    if len(adapter) != 1 or len(native) != 1 or len(readiness) != 1:
        errors.append("Stage 5E adapter/native/readiness record sets must each contain exactly one record")
    for record in [*contract, *adapter, *native, *readiness, summary]:
        for key, expected in COMMON_GUARDRAILS.items():
            if record.get(key) is not expected:
                errors.append(f"{record.get('record_type')}: {key} must be {str(expected).lower()}")
    if summary.get("selected_kernel_id") != "shift_score_kernel":
        errors.append("Stage 5E selected kernel must be shift_score_kernel")
    if summary.get("native_parity_mapped") is not True:
        errors.append("Stage 5E native parity must be mapped")
    if summary.get("implementation_readiness_status") != "ready_for_stage5f_synthetic_only_implementation":
        errors.append("Stage 5E readiness must be synthetic-only ready for Stage 5F")
    return errors
