"""Validation for Stage 5H Gematria shift contract records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.benchmark_planning.export import read_json, read_yaml, resolve_repo_path
from libreprimus.gematria_shift_contract.export import read_record_set
from libreprimus.gematria_shift_contract.models import (
    ARITHMETIC_DIRECTION,
    BAD_TRUE_FLAGS,
    CONTRACT_PATH,
    CONTRACT_SCHEMA,
    FIXTURES_PATH,
    FIXTURE_SCHEMA,
    MAPPING_PATH,
    MAPPING_SCHEMA,
    OUTPUT_DIR,
    REQUIRED_TRUE_FLAGS,
    SCORE_PLAN_PATH,
    SCORE_PLAN_SCHEMA,
    STAGE5F_HASH,
    SUMMARY_JSON,
    SUMMARY_PATH,
    SUMMARY_SCHEMA,
    TOKEN_DOMAIN,
)


def validate_stage5h_results(
    *,
    contract_path: Path = CONTRACT_PATH,
    fixtures_path: Path = FIXTURES_PATH,
    mapping_path: Path = MAPPING_PATH,
    score_summary_plan_path: Path = SCORE_PLAN_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = OUTPUT_DIR,
) -> tuple[dict[str, Any], list[str]]:
    """Validate committed and generated Stage 5H records."""

    contracts = read_record_set(contract_path)
    fixtures = read_record_set(fixtures_path)
    mappings = read_record_set(mapping_path)
    score_plans = read_record_set(score_summary_plan_path)
    summary = read_yaml(summary_path)
    generated_summary_path = resolve_repo_path(results_dir) / SUMMARY_JSON
    generated_summary = read_json(generated_summary_path) if generated_summary_path.is_file() else summary
    errors: list[str] = []
    errors.extend(_validate_records(contracts, CONTRACT_SCHEMA, "contract"))
    errors.extend(_validate_records(fixtures, FIXTURE_SCHEMA, "fixture"))
    errors.extend(_validate_records(mappings, MAPPING_SCHEMA, "mapping"))
    errors.extend(_validate_records(score_plans, SCORE_PLAN_SCHEMA, "score_plan"))
    errors.extend(_validate_one(summary, SUMMARY_SCHEMA, "summary"))
    errors.extend(_validate_one(generated_summary, SUMMARY_SCHEMA, "generated_summary"))
    if generated_summary != summary:
        errors.append("Committed Stage 5H summary does not match generated summary.json")
    records = [*contracts, *fixtures, *mappings, *score_plans, summary]
    errors.extend(_semantic_errors(records))
    fixture = fixtures[0] if fixtures else {}
    counts = {
        "contract_records": len(contracts),
        "native_fixture_records": len(fixtures),
        "solved_fixture_safe_mapping_records": len(mappings),
        "score_summary_parity_plan_records": len(score_plans),
        "contract_id": summary.get("contract_id"),
        "selected_future_kernel_id": summary.get("selected_future_kernel_id"),
        "token_domain": summary.get("token_domain"),
        "arithmetic_direction": summary.get("arithmetic_direction"),
        "separator_policy": summary.get("separator_policy"),
        "native_fixture_id": summary.get("native_fixture_id"),
        "native_fixture_hash": summary.get("native_fixture_hash"),
        "stage5f_hash_is_gematria_fixture_hash": str(fixture.get("stage5f_hash_is_gematria_fixture_hash")).lower(),
        "solved_fixture_cuda_execution_allowed": str(summary.get("solved_fixture_cuda_execution_allowed")).lower(),
        "production_gematria_mod29_cuda_ready": str(summary.get("production_gematria_mod29_cuda_ready")).lower(),
        "preflight_blocker_count": int(summary.get("preflight_blocker_count", -1)),
        "cuda_source_modified": str(summary.get("cuda_source_modified")).lower(),
        "new_cuda_kernels_added": int(summary.get("new_cuda_kernel_added", -1)),
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


def _semantic_errors(records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for record in records:
        ident = str(record.get("record_type", "record"))
        if record.get("selected_future_kernel_id") != "shift_score_kernel":
            errors.append(f"{ident}: selected_future_kernel_id must be shift_score_kernel")
        if record.get("token_domain") not in {TOKEN_DOMAIN, None}:
            errors.append(f"{ident}: token_domain must be {TOKEN_DOMAIN}")
        if record.get("arithmetic_direction") not in {ARITHMETIC_DIRECTION, None}:
            errors.append(f"{ident}: arithmetic_direction must be {ARITHMETIC_DIRECTION}")
        for key in BAD_TRUE_FLAGS:
            if record.get(key) is True:
                errors.append(f"{ident}: {key} must be false")
        for key in REQUIRED_TRUE_FLAGS:
            if record.get(key) is not True:
                errors.append(f"{ident}: {key} must be true")
        if record.get("token_domain_min") not in {0, None} or record.get("token_domain_max") not in {28, None}:
            errors.append(f"{ident}: token domain bounds must be 0..28")
        if record.get("separator_policy") in {"", None} and record.get("record_type") in {
            "gematria_shift_score_contract_record",
            "gematria_native_parity_fixture_record",
            "stage5h_gematria_shift_contract_summary",
        }:
            errors.append(f"{ident}: separator_policy is required")
        if record.get("stage5f_hash_is_gematria_fixture_hash") is True:
            errors.append(f"{ident}: Stage 5F hash must not be treated as the Gematria fixture hash")
        if record.get("expected_output_hash") == STAGE5F_HASH:
            errors.append(f"{ident}: Gematria fixture hash must differ from Stage 5F uppercase Latin hash")
        if record.get("new_cuda_kernels_added") not in {0, None}:
            errors.append(f"{ident}: new_cuda_kernels_added must be 0")
    return errors
