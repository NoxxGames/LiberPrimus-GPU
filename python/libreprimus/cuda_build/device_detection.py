"""No-GPU-safe CUDA device detection records."""

from __future__ import annotations

from pathlib import Path
import re
import shutil
import subprocess

from libreprimus.cuda_build.export import write_empty_warnings, write_record_set, write_report
from libreprimus.cuda_build.models import CUDA_BUILD_POLICY, DEVICE_PATH, DEVICE_REPORT, STAGE5C_OUTPUT_DIR


def detect_devices(
    *,
    devices_out: Path = DEVICE_PATH,
    out_dir: Path = STAGE5C_OUTPUT_DIR,
) -> list[dict[str, object]]:
    """Detect visible CUDA devices using nvidia-smi when available."""

    local_device = _query_local_device()
    local_detected = local_device is not None
    records: list[dict[str, object]] = [
        _device_record(
            device_record_id="stage5c-no-gpu-ci-profile",
            device_status="no_gpu_ci_profile",
            vram_profile="ci_no_gpu",
            gpu_model="not_required",
            memory_mib=0,
            compute_capability="",
            local_16gb_profile_detected=False,
        ),
        _device_record(
            device_record_id="stage5c-compatibility-8gb-profile",
            device_status="compatibility_profile",
            vram_profile="compatibility_8gb",
            gpu_model="generic CUDA-capable GPU",
            memory_mib=8192,
            compute_capability="",
            local_16gb_profile_detected=False,
        ),
        _device_record(
            device_record_id="stage5c-local-optional-16gb-profile",
            device_status="detected" if local_detected else "not_detected",
            vram_profile="local_optional_16gb",
            gpu_model=str(local_device.get("name", "")) if local_device else "",
            memory_mib=int(local_device.get("memory_mib", 0)) if local_device else 0,
            compute_capability=str(local_device.get("compute_capability", "")) if local_device else "",
            local_16gb_profile_detected=_is_local_16gb(local_device),
        ),
    ]
    write_record_set(devices_out, records)
    write_report(out_dir, DEVICE_REPORT, {"records": records})
    write_empty_warnings(out_dir)
    return records


def _query_local_device() -> dict[str, object] | None:
    if shutil.which("nvidia-smi") is None:
        return None
    command = [
        "nvidia-smi",
        "--query-gpu=name,memory.total,compute_cap",
        "--format=csv,noheader",
    ]
    try:
        completed = subprocess.run(command, check=False, capture_output=True, text=True, timeout=8)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if completed.returncode != 0:
        return None
    line = next((part.strip() for part in completed.stdout.splitlines() if part.strip()), "")
    if not line:
        return None
    parts = [part.strip() for part in line.split(",")]
    name = parts[0] if parts else ""
    memory_mib = _parse_mib(parts[1] if len(parts) > 1 else "")
    compute_capability = parts[2] if len(parts) > 2 else ""
    return {"name": name, "memory_mib": memory_mib, "compute_capability": compute_capability}


def _parse_mib(text: str) -> int:
    match = re.search(r"(\d+)", text)
    return int(match.group(1)) if match else 0


def _is_local_16gb(device: dict[str, object] | None) -> bool:
    if not device:
        return False
    name = str(device.get("name", "")).lower()
    memory_mib = int(device.get("memory_mib", 0))
    return "4060 ti" in name and memory_mib >= 16000


def _device_record(
    *,
    device_record_id: str,
    device_status: str,
    vram_profile: str,
    gpu_model: str,
    memory_mib: int,
    compute_capability: str,
    local_16gb_profile_detected: bool,
) -> dict[str, object]:
    return {
        "record_type": "cuda_device_detection_record",
        "stage_id": "stage-5c",
        "schema": "schemas/cuda/cuda-device-detection-record-v0.schema.json",
        "device_record_id": device_record_id,
        "device_status": device_status,
        "vram_profile": vram_profile,
        "gpu_model": gpu_model,
        "memory_mib": memory_mib,
        "compute_capability": compute_capability,
        "local_16gb_profile_detected": local_16gb_profile_detected,
        "no_gpu_ci_profile_present": True,
        **CUDA_BUILD_POLICY,
    }
