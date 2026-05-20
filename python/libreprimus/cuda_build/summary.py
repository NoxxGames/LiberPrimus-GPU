"""Stage 5C CUDA build/device summary generation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, write_yaml
from libreprimus.cuda_build.export import write_empty_warnings, write_report
from libreprimus.cuda_build.models import (
    BUILD_PROFILES_PATH,
    CUDA_BUILD_POLICY,
    DEVICE_PATH,
    SMOKE_BUILD_PATH,
    STAGE5C_OUTPUT_DIR,
    SUMMARY_PATH,
    SUMMARY_REPORT,
    TOOLCHAIN_PATH,
)


def build_summary(
    *,
    profiles_path: Path = BUILD_PROFILES_PATH,
    toolchain_path: Path = TOOLCHAIN_PATH,
    devices_path: Path = DEVICE_PATH,
    smoke_build_path: Path = SMOKE_BUILD_PATH,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = STAGE5C_OUTPUT_DIR,
) -> dict[str, Any]:
    profiles = _records(profiles_path)
    toolchain = _records(toolchain_path)
    devices = _records(devices_path)
    smoke = _records(smoke_build_path)
    toolchain_available = _toolchain_available(toolchain)
    device_available = any(record.get("device_status") == "detected" for record in devices)
    local_16gb_detected = any(record.get("local_16gb_profile_detected") is True for record in devices)
    smoke_status = _summary_smoke_status(smoke)
    summary: dict[str, Any] = {
        "record_type": "stage5c_cuda_build_device_summary",
        "schema": "schemas/cuda/stage5c-cuda-build-device-summary-v0.schema.json",
        "stage_id": "stage-5c",
        "status": "complete",
        "build_profile_records": len(profiles),
        "toolchain_detection_records": len(toolchain),
        "device_detection_records": len(devices),
        "smoke_build_records": len(smoke),
        "cuda_toolchain_available": toolchain_available,
        "cuda_device_available": device_available,
        "local_16gb_profile_detected": local_16gb_detected,
        "local_16gb_profile_required": False,
        "compatibility_8gb_profile_present": any(record.get("vram_profile") == "compatibility_8gb" for record in profiles),
        "no_gpu_ci_profile_present": any(record.get("vram_profile") == "ci_no_gpu" for record in profiles),
        "smoke_build_attempted": any(record.get("smoke_build_attempted") is True for record in smoke),
        "smoke_build_status": smoke_status,
        "next_stage": "Stage 5D - native C++ CPU batch backend and deterministic threading baseline",
        "notes": [
            "Stage 5C records CUDA build and device readiness metadata only.",
            "No CUDA kernels, GPU benchmarks, speedup claims, website expansion, raw-data processing, or solve claims were added.",
            "The local 16 GB profile is optional; CI remains no-GPU safe and the 8 GB compatibility profile remains present.",
        ],
        **CUDA_BUILD_POLICY,
    }
    write_yaml(summary_out, summary)
    write_report(out_dir, SUMMARY_REPORT, summary)
    write_empty_warnings(out_dir)
    return summary


def load_summary(summary_path: Path = SUMMARY_PATH) -> dict[str, Any]:
    return read_yaml(summary_path)


def _records(path: Path) -> list[dict[str, Any]]:
    payload = read_yaml(path)
    return list(payload.get("records", []))


def _toolchain_available(records: list[dict[str, Any]]) -> bool | str:
    statuses = {record.get("tool_id"): record.get("tool_status") for record in records}
    if not statuses:
        return "unknown"
    return statuses.get("cmake") == "detected" and statuses.get("nvcc") == "detected"


def _summary_smoke_status(records: list[dict[str, Any]]) -> str:
    if not records:
        return "skipped"
    status = str(records[0].get("smoke_build_status", "skipped_not_requested"))
    if status == "passed":
        return "passed"
    if status == "failed":
        return "failed"
    return "skipped"
