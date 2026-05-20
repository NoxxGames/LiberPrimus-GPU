"""No-GPU-safe CUDA build profile and toolchain detection."""

from __future__ import annotations

from pathlib import Path
import platform
import shutil
import subprocess

from libreprimus.cuda_build.export import write_empty_warnings, write_record_set, write_report
from libreprimus.cuda_build.models import (
    BUILD_PROFILES_PATH,
    CUDA_BUILD_POLICY,
    STAGE5C_OUTPUT_DIR,
    TOOLCHAIN_PATH,
    TOOLCHAIN_REPORT,
)


def build_profiles(
    *,
    profiles_out: Path = BUILD_PROFILES_PATH,
    out_dir: Path = STAGE5C_OUTPUT_DIR,
) -> list[dict[str, object]]:
    """Write mandatory no-GPU, 8 GB, and optional local 16 GB build profiles."""

    records: list[dict[str, object]] = [
        _profile(
            profile_id="stage5c-no-gpu-ci-profile",
            profile_status="no_gpu_ci_profile",
            vram_profile="ci_no_gpu",
            vram_gb=0,
            description="CI-compatible profile; CUDA hardware and toolkit are not required.",
        ),
        _profile(
            profile_id="stage5c-compatibility-8gb-profile",
            profile_status="compatibility_profile",
            vram_profile="compatibility_8gb",
            vram_gb=8,
            description="Future CUDA work should keep the 8 GB compatibility profile first-class.",
        ),
        _profile(
            profile_id="stage5c-local-optional-16gb-profile",
            profile_status="local_optional_profile",
            vram_profile="local_optional_16gb",
            vram_gb=16,
            description="Optional local RTX 4060 Ti 16 GB profile; never required by CI.",
        ),
    ]
    write_record_set(profiles_out, records)
    write_report(out_dir, TOOLCHAIN_REPORT, {"build_profiles": records})
    write_empty_warnings(out_dir)
    return records


def detect_toolchain(
    *,
    toolchain_out: Path = TOOLCHAIN_PATH,
    out_dir: Path = STAGE5C_OUTPUT_DIR,
) -> list[dict[str, object]]:
    """Detect CMake, nvcc, and nvidia-smi without committing absolute paths."""

    records = [
        _tool_record("cmake", ["cmake", "--version"]),
        _tool_record("nvcc", ["nvcc", "--version"]),
        _tool_record("nvidia_smi", ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"]),
    ]
    write_record_set(toolchain_out, records)
    existing_report = {"build_profiles": []}
    write_report(out_dir, TOOLCHAIN_REPORT, {**existing_report, "toolchain_records": records})
    write_empty_warnings(out_dir)
    return records


def _profile(
    *,
    profile_id: str,
    profile_status: str,
    vram_profile: str,
    vram_gb: int,
    description: str,
) -> dict[str, object]:
    return {
        "record_type": "cuda_build_profile_record",
        "stage_id": "stage-5c",
        "schema": "schemas/cuda/cuda-build-profile-record-v0.schema.json",
        "profile_id": profile_id,
        "profile_status": profile_status,
        "vram_profile": vram_profile,
        "vram_gb": vram_gb,
        "profile_description": description,
        "no_gpu_ci_profile_present": True,
        **CUDA_BUILD_POLICY,
    }


def _tool_record(tool_id: str, command: list[str]) -> dict[str, object]:
    detected = shutil.which(command[0]) is not None
    status = "missing"
    version_excerpt = ""
    if detected:
        output = _probe(command)
        status = "detected" if output is not None else "probe_failed"
        version_excerpt = _clean_excerpt(output or "")
    return {
        "record_type": "cuda_toolchain_detection_record",
        "stage_id": "stage-5c",
        "schema": "schemas/cuda/cuda-toolchain-detection-record-v0.schema.json",
        "tool_id": tool_id,
        "tool_status": status,
        "tool_detected": detected,
        "tool_required_for_ci": False,
        "absolute_path_committed": False,
        "path_marker": f"{tool_id}_detected_on_path" if detected else "",
        "version_excerpt": version_excerpt,
        "platform_summary": platform.platform(),
        **CUDA_BUILD_POLICY,
    }


def _probe(command: list[str]) -> str | None:
    try:
        completed = subprocess.run(command, check=False, capture_output=True, text=True, timeout=8)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return "\n".join(part.strip() for part in (completed.stdout, completed.stderr) if part.strip())


def _clean_excerpt(text: str) -> str:
    return text.replace("\\", "/")[:240]
