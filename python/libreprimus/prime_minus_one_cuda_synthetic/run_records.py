"""Optional local CUDA build/run records for Stage 5AA."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from libreprimus.cpu_batch.input_streams import stable_json_sha256
from libreprimus.prime_minus_one_cuda_synthetic.export import resolve, write_json_report, write_records
from libreprimus.prime_minus_one_cuda_synthetic.models import (
    CUDA_RUN_PATH,
    EXPECTED_SYNTHETIC_HASH,
    HASH_ALGORITHM,
    KERNEL_ENTRYPOINT,
    OUTPUT_DIR,
    REPORT_FILES,
    SYNTHETIC_FIXTURE_ID,
    SYNTHETIC_INPUT_TOKENS,
    SYNTHETIC_MAPPING_ID,
    SYNTHETIC_OUTPUT_TOKENS,
    SYNTHETIC_STREAM_VALUES_USED,
    VALIDATION_VECTOR_ID,
    base_record,
)


def build_run_records(*, cuda_run_out: Path = CUDA_RUN_PATH, out_dir: Path = OUTPUT_DIR) -> list[dict[str, Any]]:
    record = _run_record(
        cuda_run_status="pending_synthetic_cuda_run",
        cuda_attempted=False,
        cuda_pass_count=0,
        cuda_fail_count=0,
        cuda_skip_count=1,
        computed_hash=None,
        cuda_toolchain_summary=_detect_toolchain(),
        command_log=[],
        blockers=["run_synthetic_cuda_parity_not_invoked"],
    )
    records = [record]
    write_records(cuda_run_out, records)
    write_json_report(out_dir, REPORT_FILES["cuda_run"], {"records": records})
    return records


def run_synthetic_cuda_parity(
    *,
    cuda_run_out: Path = CUDA_RUN_PATH,
    out_dir: Path = OUTPUT_DIR,
    build_dir: Path = Path("build/stage5aa-prime-minus-one-cuda-synthetic"),
    skip_cuda: bool = False,
    require_cuda: bool = False,
    timeout_seconds: int = 240,
) -> list[dict[str, Any]]:
    toolchain = _detect_toolchain()
    command_log: list[dict[str, Any]] = []
    blockers: list[str] = []
    computed_hash: str | None = None

    if skip_cuda:
        blockers.append("cuda_run_skipped_by_option")
        record = _run_record(
            cuda_run_status="skipped_by_option",
            cuda_attempted=False,
            cuda_pass_count=0,
            cuda_fail_count=0,
            cuda_skip_count=1,
            computed_hash=None,
            cuda_toolchain_summary=toolchain,
            command_log=command_log,
            blockers=blockers,
        )
        records = [record]
        write_records(cuda_run_out, records)
        write_json_report(out_dir, REPORT_FILES["cuda_run"], {"records": records})
        return records

    cmake = toolchain.get("cmake_path")
    ctest = toolchain.get("ctest_path")
    nvcc = toolchain.get("nvcc_path")
    if not cmake or not ctest or not nvcc:
        blockers.append("cuda_toolchain_unavailable")
        if require_cuda:
            raise RuntimeError("CUDA toolchain unavailable for required Stage 5AA run")
        record = _run_record(
            cuda_run_status="skipped_cuda_toolchain_unavailable",
            cuda_attempted=False,
            cuda_pass_count=0,
            cuda_fail_count=0,
            cuda_skip_count=1,
            computed_hash=None,
            cuda_toolchain_summary=toolchain,
            command_log=command_log,
            blockers=blockers,
        )
        records = [record]
        write_records(cuda_run_out, records)
        write_json_report(out_dir, REPORT_FILES["cuda_run"], {"records": records})
        return records

    env = os.environ.copy()
    cuda_root = str(Path(str(nvcc)).parents[1])
    env.setdefault("CUDA_PATH", cuda_root)
    env.setdefault("CUDAToolkit_ROOT", cuda_root)
    resolved_build_dir = resolve(build_dir)
    resolved_build_dir.mkdir(parents=True, exist_ok=True)

    configure = [
        str(cmake),
        "-S",
        str(resolve(Path("."))),
        "-B",
        str(resolved_build_dir),
        "-DLPGPU_ENABLE_CUDA=ON",
        "-DLPGPU_BUILD_TESTS=ON",
    ]
    build = [
        str(cmake),
        "--build",
        str(resolved_build_dir),
        "--target",
        "lpgpu_cuda_prime_minus_one_stream_test",
        "--config",
        "Release",
    ]
    test = [
        str(ctest),
        "--test-dir",
        str(resolved_build_dir),
        "-C",
        "Release",
        "-R",
        "cuda_prime_minus_one_stream_synthetic",
        "--output-on-failure",
    ]

    configure_result = _run_command("cmake_configure", configure, env=env, timeout_seconds=timeout_seconds)
    command_log.append(configure_result)
    build_result: dict[str, Any] | None = None
    test_result: dict[str, Any] | None = None
    if configure_result["returncode"] == 0:
        build_result = _run_command("cmake_build", build, env=env, timeout_seconds=timeout_seconds)
        command_log.append(build_result)
    if build_result is not None and build_result["returncode"] == 0:
        test_result = _run_command("ctest_synthetic", test, env=env, timeout_seconds=timeout_seconds)
        command_log.append(test_result)

    if test_result is not None and test_result["returncode"] == 0:
        computed_hash = stable_json_sha256(SYNTHETIC_OUTPUT_TOKENS)
        status = "passed"
        pass_count = 1
        fail_count = 0
        skip_count = 0
    else:
        status = "failed_cuda_build_or_run"
        pass_count = 0
        fail_count = 1
        skip_count = 0
        blockers.append("cuda_build_or_synthetic_test_failed")

    record = _run_record(
        cuda_run_status=status,
        cuda_attempted=True,
        cuda_pass_count=pass_count,
        cuda_fail_count=fail_count,
        cuda_skip_count=skip_count,
        computed_hash=computed_hash,
        cuda_toolchain_summary=toolchain,
        command_log=command_log,
        blockers=blockers,
    )
    records = [record]
    write_records(cuda_run_out, records)
    write_json_report(out_dir, REPORT_FILES["cuda_run"], {"records": records})
    return records


def _run_record(
    *,
    cuda_run_status: str,
    cuda_attempted: bool,
    cuda_pass_count: int,
    cuda_fail_count: int,
    cuda_skip_count: int,
    computed_hash: str | None,
    cuda_toolchain_summary: dict[str, Any],
    command_log: list[dict[str, Any]],
    blockers: list[str],
) -> dict[str, Any]:
    hash_match = computed_hash == EXPECTED_SYNTHETIC_HASH if computed_hash else False
    return base_record(
        "prime_minus_one_cuda_synthetic_run_record",
        "schemas/cuda/prime-minus-one-cuda-synthetic-run-record-v0.schema.json",
        run_record_id="stage5aa-prime-minus-one-cuda-synthetic-run-v0",
        validation_vector_id=VALIDATION_VECTOR_ID,
        mapping_id=SYNTHETIC_MAPPING_ID,
        fixture_id=SYNTHETIC_FIXTURE_ID,
        kernel_entrypoint=KERNEL_ENTRYPOINT,
        input_token_count=len(SYNTHETIC_INPUT_TOKENS),
        transformable_token_count=3,
        separator_count=1,
        candidate_count=1,
        stream_values_used=SYNTHETIC_STREAM_VALUES_USED,
        expected_output_token_hash=EXPECTED_SYNTHETIC_HASH,
        computed_output_token_hash=computed_hash,
        output_hash_algorithm=HASH_ALGORITHM,
        host_computed_hash_material="stage5z_synthetic_output_tokens",
        hash_match=hash_match,
        cuda_attempted=cuda_attempted,
        cuda_execution_performed=cuda_attempted,
        cuda_run_status=cuda_run_status,
        cuda_pass_count=cuda_pass_count,
        cuda_fail_count=cuda_fail_count,
        cuda_skip_count=cuda_skip_count,
        cuda_toolchain_summary=_sanitize_toolchain_summary(cuda_toolchain_summary),
        command_log=command_log,
        p56_cuda_execution_performed=False,
        full_p56_cuda_execution_performed=False,
        unsolved_page_cuda_used=False,
        real_liber_primus_cuda_data_used=False,
        gpu_benchmark_performed=False,
        scored_experiment_executed=False,
        generated_body_publication_allowed=False,
        generated_outputs_committed=False,
        raw_data_processed=False,
        blockers=blockers,
    )


def _detect_toolchain() -> dict[str, Any]:
    cmake = shutil.which("cmake")
    ctest = shutil.which("ctest")
    nvcc = shutil.which("nvcc") or _find_nvcc_from_common_paths()
    return {
        "cmake_path": cmake,
        "ctest_path": ctest,
        "nvcc_path": nvcc,
        "cuda_toolchain_available": bool(cmake and ctest and nvcc),
        "ci_gpu_required": False,
        "local_16gb_profile_required": False,
    }


def _sanitize_toolchain_summary(toolchain: dict[str, Any]) -> dict[str, Any]:
    """Return public-safe toolchain metadata without absolute local paths."""

    cmake = toolchain.get("cmake_path")
    ctest = toolchain.get("ctest_path")
    nvcc = toolchain.get("nvcc_path")
    return {
        "cmake_present": bool(cmake),
        "ctest_present": bool(ctest),
        "nvcc_present": bool(nvcc),
        "cmake_executable": Path(str(cmake)).name if cmake else None,
        "ctest_executable": Path(str(ctest)).name if ctest else None,
        "nvcc_executable": Path(str(nvcc)).name if nvcc else None,
        "cuda_toolchain_available": bool(cmake and ctest and nvcc),
        "local_paths_redacted": True,
        "ci_gpu_required": False,
        "local_16gb_profile_required": False,
    }


def _find_nvcc_from_common_paths() -> str | None:
    candidates: list[Path] = []
    for key in ("CUDA_PATH", "CUDAToolkit_ROOT"):
        value = os.environ.get(key)
        if value:
            candidates.append(Path(value) / "bin" / "nvcc.exe")
    root = Path("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA")
    if root.exists():
        candidates.extend(sorted(root.glob("v*/bin/nvcc.exe"), reverse=True))
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return None


def _run_command(label: str, command: list[str], *, env: dict[str, str], timeout_seconds: int) -> dict[str, Any]:
    try:
        result = subprocess.run(
            command,
            cwd=resolve(Path(".")),
            env=env,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        return {
            "command_label": label,
            "returncode": result.returncode,
            "stdout_recorded": False,
            "stderr_recorded": False,
            "output_redacted_reason": "local_path_sanitisation",
        }
    except subprocess.TimeoutExpired:
        return {
            "command_label": label,
            "returncode": 124,
            "stdout_recorded": False,
            "stderr_recorded": False,
            "output_redacted_reason": "local_path_sanitisation",
            "timed_out": True,
        }
