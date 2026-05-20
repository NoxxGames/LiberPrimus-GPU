"""Optional no-GPU-safe CUDA build records for Stage 5F."""

from __future__ import annotations

from pathlib import Path
import os
import shutil
import subprocess
from typing import Any

from libreprimus.benchmark_planning.export import resolve_repo_path
from libreprimus.cuda_kernel.export import write_record_set, write_report, write_warnings
from libreprimus.cuda_kernel.models import BUILD_DIR, BUILD_RECORDS_PATH, BUILD_REPORT, COMMON_POLICY_FLAGS, OUTPUT_DIR, STAGE_ID
from libreprimus.paths import repo_root


def build_records(
    *,
    build_records_out: Path = BUILD_RECORDS_PATH,
    out_dir: Path = OUTPUT_DIR,
    build_dir: Path = BUILD_DIR,
    require_cuda: bool = False,
    run_build: bool = True,
) -> list[dict[str, Any]]:
    cmake_detected = shutil.which("cmake") is not None
    nvcc_path = shutil.which("nvcc")
    nvcc_detected = nvcc_path is not None
    status = "skipped_not_requested"
    attempted = False
    configure_return_code: int | None = None
    build_return_code: int | None = None
    failure_reason = ""
    if not run_build:
        status = "skipped_not_requested"
    elif not (cmake_detected and nvcc_detected):
        status = "failed_missing_cuda" if require_cuda else "skipped_missing_cuda"
        failure_reason = "cmake_or_nvcc_missing"
    else:
        attempted = True
        status, configure_return_code, build_return_code, failure_reason = _configure_and_build(resolve_repo_path(build_dir), nvcc_path)
    record: dict[str, Any] = {
        "record_type": "cuda_kernel_build_record",
        "stage_id": STAGE_ID,
        "build_record_id": "stage5f-shift-score-cuda-build",
        "build_status": status,
        "cuda_build_attempted": attempted,
        "cmake_detected": cmake_detected,
        "nvcc_detected": nvcc_detected,
        "configure_return_code": configure_return_code,
        "build_return_code": build_return_code,
        "failure_reason": failure_reason,
        "build_dir_kind": "ignored_stage5f_cuda_build",
        "target": "lpgpu_cuda_shift_score_test",
        "cuda_kernel_added": True,
        "cuda_source_modified": True,
        "cuda_transform_executed": False,
        "native_reference_hash": "76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66",
        **COMMON_POLICY_FLAGS,
    }
    records = [record]
    write_record_set(build_records_out, records)
    write_report(out_dir, BUILD_REPORT, {"records": records})
    write_warnings(out_dir, [] if status != "failed" else [{"level": "warning", "message": failure_reason or "cuda_build_failed"}])
    if require_cuda and status != "passed":
        raise RuntimeError(f"CUDA build required but status is {status}: {failure_reason}")
    return records


def _configure_and_build(build_dir: Path, nvcc_path: str | None) -> tuple[str, int | None, int | None, str]:
    build_dir.mkdir(parents=True, exist_ok=True)
    configure_command = [
        "cmake",
        "-S",
        str(repo_root()),
        "-B",
        str(build_dir),
        "-DLPGPU_ENABLE_CUDA=ON",
        "-DLPGPU_BUILD_TESTS=ON",
        "-DLPGPU_BUILD_CLI=OFF",
        "-DCMAKE_CUDA_ARCHITECTURES=89",
    ]
    if nvcc_path and os.name == "nt":
        toolkit_root = Path(nvcc_path).resolve().parents[1]
        configure_command[1:1] = ["-T", f"cuda={toolkit_root}"]
    elif nvcc_path:
        configure_command.append(f"-DCMAKE_CUDA_COMPILER={nvcc_path}")
    configure = subprocess.run(
        configure_command,
        check=False,
        capture_output=True,
        text=True,
        timeout=180,
    )
    if configure.returncode != 0:
        return "failed", configure.returncode, None, _tail(configure.stdout, configure.stderr)
    build = subprocess.run(
        ["cmake", "--build", str(build_dir), "--target", "lpgpu_cuda_shift_score_test", "--config", "Debug"],
        check=False,
        capture_output=True,
        text=True,
        timeout=240,
    )
    if build.returncode != 0:
        return "failed", configure.returncode, build.returncode, _tail(build.stdout, build.stderr)
    return "passed", configure.returncode, build.returncode, ""


def _tail(*parts: str) -> str:
    text = "\n".join(part for part in parts if part)
    return "\n".join(text.splitlines()[-8:])[:1200]
