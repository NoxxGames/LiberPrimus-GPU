"""Optional local CUDA build records for Stage 5J."""

from __future__ import annotations

from pathlib import Path
import os
import shutil
import subprocess
from typing import Any

from libreprimus.benchmark_planning.export import resolve_repo_path
from libreprimus.gematria_cuda_kernel.export import write_record_set, write_report, write_warnings
from libreprimus.gematria_cuda_kernel.models import BUILD_DIR, BUILD_RECORDS_PATH, BUILD_REPORT, COMMON_POLICY_FLAGS, OUTPUT_DIR
from libreprimus.paths import repo_root


def build_records(
    *,
    build_records_out: Path = BUILD_RECORDS_PATH,
    out_dir: Path = OUTPUT_DIR,
    build_dir: Path = BUILD_DIR,
    require_cuda: bool = False,
    run_build: bool = True,
) -> list[dict[str, Any]]:
    """Attempt the optional Stage 5J CUDA build, or record an explicit no-GPU skip."""

    cmake_path = shutil.which("cmake")
    nvcc_path = _find_nvcc()
    cmake_detected = cmake_path is not None
    nvcc_detected = nvcc_path is not None
    attempted = False
    configure_return_code: int | None = None
    build_return_code: int | None = None
    failure_reason = ""
    toolkit_root = _toolkit_root(nvcc_path)
    status = "skipped_not_requested"

    if not run_build:
        status = "skipped_not_requested"
    elif not (cmake_detected and nvcc_detected):
        status = "failed_missing_cuda" if require_cuda else "skipped_missing_cuda"
        failure_reason = "cmake_or_nvcc_missing"
    else:
        attempted = True
        status, configure_return_code, build_return_code, failure_reason = _configure_and_build(
            resolve_repo_path(build_dir),
            nvcc_path,
        )

    record: dict[str, Any] = {
        "record_type": "gematria_cuda_kernel_build_record",
        "build_record_id": "stage5j-gematria-cuda-kernel-build",
        "build_status": status,
        "cuda_build_attempted": attempted,
        "cmake_detected": cmake_detected,
        "cmake_path": _sanitized_tool_label(cmake_path, "cmake"),
        "nvcc_detected": nvcc_detected,
        "nvcc_path": _sanitized_tool_label(nvcc_path, "nvcc"),
        "toolkit_root": "local_cuda_toolkit_detected" if toolkit_root is not None else "",
        "configure_return_code": configure_return_code,
        "build_return_code": build_return_code,
        "failure_reason": failure_reason,
        "build_dir_kind": "ignored_stage5j_cuda_build",
        "target": "lpgpu_cuda_gematria_shift_score_test",
        "cuda_execution_performed": False,
        **COMMON_POLICY_FLAGS,
    }
    records = [record]
    write_record_set(build_records_out, records)
    write_report(out_dir, BUILD_REPORT, {"records": records})
    warnings = [] if status in {"passed", "skipped_not_requested", "skipped_missing_cuda"} else [{"level": "warning", "message": failure_reason or status}]
    write_warnings(out_dir, warnings)
    if require_cuda and status != "passed":
        raise RuntimeError(f"CUDA build required but status is {status}: {failure_reason}")
    return records


def _find_nvcc() -> str | None:
    detected = shutil.which("nvcc")
    if detected:
        return detected
    if os.name != "nt":
        return None
    root = Path("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA")
    if not root.exists():
        return None
    candidates = sorted(root.glob("v*/bin/nvcc.exe"), reverse=True)
    return str(candidates[0]) if candidates else None


def _toolkit_root(nvcc_path: str | None) -> Path | None:
    if not nvcc_path:
        return None
    return Path(nvcc_path).resolve().parents[1]


def _sanitized_tool_label(path: str | None, tool_name: str) -> str:
    if not path:
        return ""
    suffix = Path(path).suffix
    return f"{tool_name}{suffix} detected"


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
        toolkit_root = _toolkit_root(nvcc_path)
        if toolkit_root is not None:
            configure_command[1:1] = ["-T", f"cuda={toolkit_root}"]
    elif nvcc_path:
        configure_command.append(f"-DCMAKE_CUDA_COMPILER={nvcc_path}")
    configure = subprocess.run(configure_command, check=False, capture_output=True, text=True, timeout=180)
    if configure.returncode != 0:
        failure = _tail(configure.stdout, configure.stderr)
        return _classify_configure_failure(failure), configure.returncode, None, failure
    build = subprocess.run(
        ["cmake", "--build", str(build_dir), "--target", "lpgpu_cuda_gematria_shift_score_test", "--config", "Debug"],
        check=False,
        capture_output=True,
        text=True,
        timeout=240,
    )
    if build.returncode != 0:
        failure = _tail(build.stdout, build.stderr)
        return "failed", configure.returncode, build.returncode, failure
    return "passed", configure.returncode, build.returncode, ""


def _classify_configure_failure(text: str) -> str:
    lowered = text.lower()
    if "could not find" in lowered and "cuda" in lowered:
        return "failed_toolkit_resolution"
    if "cuda toolkit directory" in lowered or "toolkit" in lowered:
        return "failed_toolkit_resolution"
    return "failed_environment"


def _tail(*parts: str) -> str:
    text = "\n".join(part for part in parts if part)
    return "\n".join(text.splitlines()[-10:])[:1600]
