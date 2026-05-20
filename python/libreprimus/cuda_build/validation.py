"""Validation for Stage 5C CUDA build/device detection records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.benchmark_planning.export import read_json, read_yaml, resolve_repo_path
from libreprimus.cuda_build.models import (
    BAD_TRUE_FLAGS,
    BUILD_PROFILE_SCHEMA,
    BUILD_PROFILES_PATH,
    DEVICE_PATH,
    DEVICE_SCHEMA,
    SMOKE_BUILD_PATH,
    SMOKE_BUILD_SCHEMA,
    STAGE5C_OUTPUT_DIR,
    SUMMARY_PATH,
    SUMMARY_REPORT,
    SUMMARY_SCHEMA,
    TOOLCHAIN_PATH,
    TOOLCHAIN_SCHEMA,
)


def validate_stage5c_results(
    *,
    profiles_path: Path = BUILD_PROFILES_PATH,
    toolchain_path: Path = TOOLCHAIN_PATH,
    devices_path: Path = DEVICE_PATH,
    smoke_build_path: Path = SMOKE_BUILD_PATH,
    summary_path: Path = SUMMARY_PATH,
    results_dir: Path = STAGE5C_OUTPUT_DIR,
) -> tuple[dict[str, int | str | bool], list[str]]:
    profiles = _records(profiles_path)
    toolchain = _records(toolchain_path)
    devices = _records(devices_path)
    smoke = _records(smoke_build_path)
    summary = read_yaml(summary_path)
    generated_summary = read_json(resolve_repo_path(results_dir) / SUMMARY_REPORT)
    errors: list[str] = []
    errors.extend(_validate_records(profiles, BUILD_PROFILE_SCHEMA, "profiles"))
    errors.extend(_validate_records(toolchain, TOOLCHAIN_SCHEMA, "toolchain"))
    errors.extend(_validate_records(devices, DEVICE_SCHEMA, "devices"))
    errors.extend(_validate_records(smoke, SMOKE_BUILD_SCHEMA, "smoke"))
    errors.extend(_validate_one(summary, SUMMARY_SCHEMA, "summary"))
    errors.extend(_validate_one(generated_summary, SUMMARY_SCHEMA, "generated_summary"))
    if summary != generated_summary:
        errors.append("Committed Stage 5C summary does not match generated summary.json")
    errors.extend(_policy_errors([*profiles, *toolchain, *devices, *smoke, summary]))
    errors.extend(_semantic_errors(profiles, toolchain, devices, smoke, summary))
    counts: dict[str, int | str | bool] = {
        "build_profiles": len(profiles),
        "toolchain_records": len(toolchain),
        "device_records": len(devices),
        "smoke_build_records": len(smoke),
        "cuda_toolchain_available": summary.get("cuda_toolchain_available", "unknown"),
        "cuda_device_available": summary.get("cuda_device_available", "unknown"),
        "local_16gb_profile_detected": summary.get("local_16gb_profile_detected", "unknown"),
        "local_16gb_profile_required": summary.get("local_16gb_profile_required", False),
        "compatibility_8gb_profile_present": summary.get("compatibility_8gb_profile_present", False),
        "no_gpu_ci_profile_present": summary.get("no_gpu_ci_profile_present", False),
        "smoke_build_attempted": summary.get("smoke_build_attempted", False),
        "smoke_build_status": str(summary.get("smoke_build_status", "skipped")),
    }
    return counts, errors


def _records(path: Path) -> list[dict[str, Any]]:
    return list(read_yaml(path).get("records", []))


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


def _policy_errors(records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for record in records:
        ident = str(
            record.get("profile_id")
            or record.get("tool_id")
            or record.get("device_record_id")
            or record.get("smoke_build_id")
            or record.get("record_type")
        )
        for key in BAD_TRUE_FLAGS:
            if record.get(key) is True:
                errors.append(f"{ident}: {key} must be false")
        if record.get("no_solve_claim") is not True:
            errors.append(f"{ident}: no_solve_claim must be true")
    return errors


def _semantic_errors(
    profiles: list[dict[str, Any]],
    toolchain: list[dict[str, Any]],
    devices: list[dict[str, Any]],
    smoke: list[dict[str, Any]],
    summary: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    profile_ids = {record.get("vram_profile") for record in profiles}
    if not {"ci_no_gpu", "compatibility_8gb", "local_optional_16gb"}.issubset(profile_ids):
        errors.append("Missing one or more required Stage 5C build profiles")
    tool_ids = {record.get("tool_id") for record in toolchain}
    if not {"cmake", "nvcc", "nvidia_smi"}.issubset(tool_ids):
        errors.append("Missing one or more required Stage 5C toolchain records")
    device_profiles = {record.get("vram_profile") for record in devices}
    if not {"ci_no_gpu", "compatibility_8gb", "local_optional_16gb"}.issubset(device_profiles):
        errors.append("Missing one or more required Stage 5C device profile records")
    if len(smoke) != 1:
        errors.append("Stage 5C must contain exactly one smoke-build record")
    if summary.get("build_profile_records") != len(profiles):
        errors.append("build profile count mismatch")
    if summary.get("toolchain_detection_records") != len(toolchain):
        errors.append("toolchain count mismatch")
    if summary.get("device_detection_records") != len(devices):
        errors.append("device count mismatch")
    if summary.get("smoke_build_records") != len(smoke):
        errors.append("smoke-build count mismatch")
    if summary.get("local_16gb_profile_required") is not False:
        errors.append("local_16gb_profile_required must be false")
    return errors
