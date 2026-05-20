"""Best-effort CUDA backend capability records for Stage 5B."""

from __future__ import annotations

from pathlib import Path
import platform
import shutil
import subprocess

from libreprimus.cuda_parity.export import write_empty_warnings, write_record_set, write_report
from libreprimus.cuda_parity.models import (
    BACKEND_CAPABILITY_PATH,
    BACKEND_REPORT,
    CUDA_PARITY_POLICY,
    STAGE5B_OUTPUT_DIR,
)


def build_backend_capability(
    *,
    out_dir: Path = STAGE5B_OUTPUT_DIR,
    backend_capability_out: Path = BACKEND_CAPABILITY_PATH,
    local_gpu_model: str = "NVIDIA RTX 4060 Ti",
    local_vram_gb: int = 16,
) -> list[dict[str, object]]:
    """Build backend capability records without requiring CUDA hardware."""

    nvcc_path = shutil.which("nvcc")
    nvidia_smi_path = shutil.which("nvidia-smi")
    nvcc_version = _probe([nvcc_path, "--version"]) if nvcc_path else ""
    smi_output = _probe([nvidia_smi_path, "--query-gpu=name,memory.total", "--format=csv,noheader"]) if nvidia_smi_path else ""
    detected_device = bool(smi_output.strip())
    toolkit_detected = bool(nvcc_version.strip())
    local_status = "cuda_device_detected" if detected_device else "cuda_available_unverified"
    if toolkit_detected and not detected_device:
        local_status = "cuda_toolkit_detected"
    records: list[dict[str, object]] = [
        _record(
            backend_id="stage5b-ci-no-gpu-profile",
            backend_status="cuda_hardware_not_required",
            vram_profile="ci_no_gpu",
            gpu_model="not_required",
            vram_gb=0,
            local_16gb_profile_supported=False,
            nvcc_path="",
            nvidia_smi_path="",
            probe_notes=["CI validation must pass without CUDA hardware or toolkit."],
        ),
        _record(
            backend_id="stage5b-compatibility-8gb-profile",
            backend_status="cuda_hardware_not_required",
            vram_profile="compatibility_8gb",
            gpu_model="generic CUDA-capable GPU",
            vram_gb=8,
            local_16gb_profile_supported=False,
            nvcc_path="",
            nvidia_smi_path="",
            probe_notes=["Eight GB remains the compatibility planning profile; Stage 5B does not allocate GPU memory."],
        ),
        _record(
            backend_id="stage5b-local-rtx-4060-ti-16gb-profile",
            backend_status=local_status,
            vram_profile="local_16gb",
            gpu_model=local_gpu_model,
            vram_gb=local_vram_gb,
            local_16gb_profile_supported=True,
            nvcc_path=_tool_marker(nvcc_path, "nvcc"),
            nvidia_smi_path=_tool_marker(nvidia_smi_path, "nvidia-smi"),
            probe_notes=[
                "Local RTX 4060 Ti 16 GB is planning metadata only and is not required by CI or future users.",
                f"nvcc_detected={str(toolkit_detected).lower()}",
                f"nvidia_smi_detected={str(detected_device).lower()}",
                f"platform={platform.platform()}",
                f"nvcc_version={nvcc_version[:160]}",
                f"nvidia_smi={smi_output[:160]}",
            ],
        ),
    ]
    write_record_set(backend_capability_out, records)
    write_report(out_dir, BACKEND_REPORT, {"records": records})
    write_empty_warnings(out_dir)
    return records


def _probe(command: list[str | None]) -> str:
    argv = [part for part in command if part]
    if not argv:
        return ""
    try:
        completed = subprocess.run(argv, check=False, capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return "\n".join(part.strip() for part in (completed.stdout, completed.stderr) if part.strip())


def _tool_marker(path: str | None, tool_name: str) -> str:
    """Record tool presence without committing a machine-specific absolute path."""

    return f"{tool_name}_detected_on_path" if path else ""


def _record(
    *,
    backend_id: str,
    backend_status: str,
    vram_profile: str,
    gpu_model: str,
    vram_gb: int,
    local_16gb_profile_supported: bool,
    nvcc_path: str,
    nvidia_smi_path: str,
    probe_notes: list[str],
) -> dict[str, object]:
    return {
        "record_type": "cuda_backend_capability_record",
        "stage_id": "stage-5b",
        "backend_id": backend_id,
        "backend_status": backend_status,
        "vram_profile": vram_profile,
        "gpu_model": gpu_model,
        "vram_gb": vram_gb,
        "compute_capability_planned": "8.9" if vram_profile == "local_16gb" else "",
        "local_16gb_profile_supported": local_16gb_profile_supported,
        "local_16gb_profile_required": False,
        "cuda_hardware_required": False,
        "nvcc_path": nvcc_path,
        "nvidia_smi_path": nvidia_smi_path,
        "probe_notes": probe_notes,
        **CUDA_PARITY_POLICY,
    }
