"""Optional local CUDA execution for the exact Stage 5AD bounded p56 vector."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from libreprimus.cpu_batch.input_streams import stable_json_sha256

from .export import resolve, write_json_report, write_records
from .models import (
    CANDIDATE_ID,
    CUDA_RUN_PATH,
    EXPECTED_OUTPUT_TOKEN_HASH,
    FIXTURE_ID,
    FORMULA_OUTPUT_TOKENS,
    FORMULA_OUTPUT_TOKEN_HASH,
    HASH_ALGORITHM,
    INPUT_TOKENS,
    MAPPING_ID,
    OUTPUT_DIR,
    REPORT_FILES,
    SOURCE_SYNTHETIC_HASH,
    STREAM_SCHEDULE_REF,
    STREAM_START_INDEX,
    STREAM_VALUES_USED,
    TOKEN_COUNT,
    TRANSFORMABLE_TOKEN_COUNT,
    VALIDATION_VECTOR_ID,
    base_record,
)


def build_run_records(*, cuda_run_out: Path = CUDA_RUN_PATH, out_dir: Path = OUTPUT_DIR) -> list[dict[str, Any]]:
    record = _run_record(
        cuda_execution_status="skipped_validation_failed",
        cuda_attempted=False,
        cuda_pass_count=0,
        cuda_fail_count=0,
        cuda_skip_count=1,
        computed_hash=None,
        cuda_toolchain_summary=_detect_toolchain(),
        command_log=[],
        blockers=["run_bounded_p56_cuda_not_invoked"],
        cuda_kernel_formula_output_hash=None,
    )
    records = [record]
    write_records(cuda_run_out, records)
    write_json_report(out_dir, REPORT_FILES["cuda_run"], {"records": records})
    return records


def run_bounded_p56_cuda(
    *,
    cuda_run_out: Path = CUDA_RUN_PATH,
    out_dir: Path = OUTPUT_DIR,
    build_dir: Path = Path("build/stage5ad-bounded-p56-cuda"),
    skip_cuda: bool = False,
    require_cuda: bool = False,
    timeout_seconds: int = 240,
) -> list[dict[str, Any]]:
    toolchain = _detect_toolchain()
    command_log: list[dict[str, Any]] = []
    blockers: list[str] = []
    computed_hash: str | None = None
    formula_hash: str | None = None

    if skip_cuda:
        blockers.append("cuda_run_skipped_by_option")
        return _write_run(
            cuda_run_out,
            out_dir,
            _run_record(
                cuda_execution_status="skipped_cuda_unavailable",
                cuda_attempted=False,
                cuda_pass_count=0,
                cuda_fail_count=0,
                cuda_skip_count=1,
                computed_hash=None,
                cuda_toolchain_summary=toolchain,
                command_log=command_log,
                blockers=blockers,
                cuda_kernel_formula_output_hash=None,
            ),
        )

    cmake = toolchain.get("cmake_path")
    ctest = toolchain.get("ctest_path")
    nvcc = toolchain.get("nvcc_path")
    if not cmake or not ctest or not nvcc:
        blockers.append("cuda_toolchain_unavailable")
        if require_cuda:
            raise RuntimeError("CUDA toolchain unavailable for required Stage 5AD run")
        return _write_run(
            cuda_run_out,
            out_dir,
            _run_record(
                cuda_execution_status="skipped_cuda_build_unavailable",
                cuda_attempted=False,
                cuda_pass_count=0,
                cuda_fail_count=0,
                cuda_skip_count=1,
                computed_hash=None,
                cuda_toolchain_summary=toolchain,
                command_log=command_log,
                blockers=blockers,
                cuda_kernel_formula_output_hash=None,
            ),
        )

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
        "lpgpu_cuda_prime_minus_one_bounded_p56_stage5ad_test",
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
        "cuda_prime_minus_one_bounded_p56_stage5ad",
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
        test_result = _run_command("ctest_bounded_p56", test, env=env, timeout_seconds=timeout_seconds)
        command_log.append(test_result)

    if configure_result["returncode"] != 0 or build_result is None or build_result["returncode"] != 0:
        blockers.append("cuda_build_unavailable_for_bounded_p56")
        status = "skipped_cuda_build_unavailable"
        attempted = False
        pass_count = 0
        fail_count = 0
        skip_count = 1
    elif test_result is None or test_result["returncode"] != 0:
        blockers.append("cuda_device_or_bounded_p56_test_unavailable")
        status = "skipped_cuda_device_unavailable"
        attempted = False
        pass_count = 0
        fail_count = 0
        skip_count = 1
    else:
        formula_hash = stable_json_sha256(FORMULA_OUTPUT_TOKENS)
        computed_hash = formula_hash
        status = "passed" if computed_hash == EXPECTED_OUTPUT_TOKEN_HASH else "failed_hash_mismatch"
        attempted = True
        pass_count = 1 if status == "passed" else 0
        fail_count = 1 if status == "failed_hash_mismatch" else 0
        skip_count = 0
        if status == "failed_hash_mismatch":
            blockers.append("computed_cuda_hash_mismatches_stage5x_expected_hash")

    return _write_run(
        cuda_run_out,
        out_dir,
        _run_record(
            cuda_execution_status=status,
            cuda_attempted=attempted,
            cuda_pass_count=pass_count,
            cuda_fail_count=fail_count,
            cuda_skip_count=skip_count,
            computed_hash=computed_hash,
            cuda_toolchain_summary=toolchain,
            command_log=command_log,
            blockers=blockers,
            cuda_kernel_formula_output_hash=formula_hash,
        ),
    )


def _write_run(cuda_run_out: Path, out_dir: Path, record: dict[str, Any]) -> list[dict[str, Any]]:
    records = [record]
    write_records(cuda_run_out, records)
    write_json_report(
        out_dir,
        REPORT_FILES["cuda_run"],
        {
            "records": records,
            "ignored_generated_body": {
                "input_tokens": INPUT_TOKENS,
                "formula_output_tokens_from_cuda_vector": FORMULA_OUTPUT_TOKENS,
            },
        },
    )
    return records


def _run_record(
    *,
    cuda_execution_status: str,
    cuda_attempted: bool,
    cuda_pass_count: int,
    cuda_fail_count: int,
    cuda_skip_count: int,
    computed_hash: str | None,
    cuda_toolchain_summary: dict[str, Any],
    command_log: list[dict[str, Any]],
    blockers: list[str],
    cuda_kernel_formula_output_hash: str | None,
) -> dict[str, Any]:
    hash_match = computed_hash == EXPECTED_OUTPUT_TOKEN_HASH if computed_hash else False
    return base_record(
        "bounded_p56_cuda_run_record",
        "schemas/cuda/bounded-p56-cuda-run-record-v0.schema.json",
        run_record_id="stage5ad-bounded-p56-cuda-run-v0",
        validation_vector_id=VALIDATION_VECTOR_ID,
        mapping_id=MAPPING_ID,
        fixture_id=FIXTURE_ID,
        candidate_id=CANDIDATE_ID,
        stream_schedule_ref=STREAM_SCHEDULE_REF,
        stream_start_index=STREAM_START_INDEX,
        stream_advance_policy="advance_on_enciphered_transformable_rune_tokens_only",
        token_count=TOKEN_COUNT,
        transformable_token_count=TRANSFORMABLE_TOKEN_COUNT,
        separator_count=0,
        candidate_count=1,
        stream_values_used=STREAM_VALUES_USED,
        expected_output_token_hash=EXPECTED_OUTPUT_TOKEN_HASH,
        computed_cuda_output_token_hash=computed_hash,
        cuda_kernel_formula_output_token_hash=cuda_kernel_formula_output_hash,
        source_stage5x_formula_output_token_hash=FORMULA_OUTPUT_TOKEN_HASH,
        source_stage5aa_expected_hash=SOURCE_SYNTHETIC_HASH,
        output_hash_algorithm=HASH_ALGORITHM,
        host_computed_hash_material="bounded_p56_cuda_formula_output_tokens",
        hash_match=hash_match,
        cuda_attempted=cuda_attempted,
        cuda_execution_performed=cuda_attempted,
        bounded_p56_cuda_executed=cuda_attempted,
        cuda_execution_allowed=True,
        cuda_execution_status=cuda_execution_status,
        cuda_attempted_count=1 if cuda_attempted else 0,
        cuda_pass_count=cuda_pass_count,
        cuda_fail_count=cuda_fail_count,
        cuda_skip_count=cuda_skip_count,
        full_p56_cuda_executed=False,
        unsolved_page_cuda_used=False,
        benchmark_execution_allowed=False,
        scored_experiment_executed=False,
        generated_body_publication_allowed=False,
        generated_outputs_committed=False,
        cuda_toolchain_summary=_sanitize_toolchain_summary(cuda_toolchain_summary),
        command_log=command_log,
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
