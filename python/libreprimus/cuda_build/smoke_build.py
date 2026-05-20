"""Optional CUDA smoke-build record generation."""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess

from libreprimus.benchmark_planning.export import resolve_repo_path
from libreprimus.cuda_build.export import write_empty_warnings, write_record_set, write_report
from libreprimus.cuda_build.models import CUDA_BUILD_POLICY, SMOKE_BUILD_PATH, SMOKE_BUILD_REPORT, STAGE5C_OUTPUT_DIR
from libreprimus.paths import repo_root


def run_smoke_build(
    *,
    smoke_build_out: Path = SMOKE_BUILD_PATH,
    out_dir: Path = STAGE5C_OUTPUT_DIR,
    attempt_build: bool = False,
) -> list[dict[str, object]]:
    """Optionally configure/build the existing CUDA smoke target without running it."""

    status = "skipped_not_requested"
    configure_return_code: int | None = None
    build_return_code: int | None = None
    cmake_detected = shutil.which("cmake") is not None
    nvcc_detected = shutil.which("nvcc") is not None
    if attempt_build and not (cmake_detected and nvcc_detected):
        status = "skipped_missing_cuda"
    elif attempt_build:
        status, configure_return_code, build_return_code = _configure_and_build(resolve_repo_path(out_dir))
    record = {
        "record_type": "cuda_smoke_build_record",
        "stage_id": "stage-5c",
        "schema": "schemas/cuda/cuda-smoke-build-record-v0.schema.json",
        "smoke_build_id": "stage5c-optional-cuda-smoke-build",
        "smoke_build_status": status,
        "smoke_build_attempted": attempt_build and status in {"passed", "failed"},
        "smoke_test_executed": False,
        "cmake_detected": cmake_detected,
        "nvcc_detected": nvcc_detected,
        "configure_return_code": configure_return_code,
        "build_return_code": build_return_code,
        "build_dir_kind": "ignored_generated_stage5c_cmake_smoke_build",
        "target": "lpgpu_cuda_smoke",
        **CUDA_BUILD_POLICY,
    }
    records = [record]
    write_record_set(smoke_build_out, records)
    write_report(out_dir, SMOKE_BUILD_REPORT, {"records": records})
    write_empty_warnings(out_dir)
    return records


def _configure_and_build(out_dir: Path) -> tuple[str, int | None, int | None]:
    build_dir = out_dir / "cmake-smoke-build"
    build_dir.mkdir(parents=True, exist_ok=True)
    configure = subprocess.run(
        [
            "cmake",
            "-S",
            str(repo_root()),
            "-B",
            str(build_dir),
            "-DLPGPU_ENABLE_CUDA=ON",
            "-DLPGPU_BUILD_TESTS=OFF",
            "-DLPGPU_BUILD_CLI=OFF",
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if configure.returncode != 0:
        return "failed", configure.returncode, None
    build = subprocess.run(
        ["cmake", "--build", str(build_dir), "--target", "lpgpu_cuda_smoke", "--config", "Release"],
        check=False,
        capture_output=True,
        text=True,
        timeout=180,
    )
    return ("passed" if build.returncode == 0 else "failed"), configure.returncode, build.returncode
