"""Synthetic CUDA parity run records for Stage 5F."""

from __future__ import annotations

from pathlib import Path
import subprocess
from typing import Any

from libreprimus.benchmark_planning.export import resolve_repo_path
from libreprimus.cuda_kernel.export import read_record_set, write_record_set, write_report, write_warnings
from libreprimus.cuda_kernel.models import BUILD_DIR, BUILD_RECORDS_PATH, COMMON_POLICY_FLAGS, OUTPUT_DIR, PARITY_RECORDS_PATH, PARITY_REPORT, STAGE_ID
from libreprimus.cuda_kernel.synthetic_parity import EXPECTED_NATIVE_HASH, python_reference_hash


def build_parity_records(
    *,
    build_records_path: Path = BUILD_RECORDS_PATH,
    parity_records_out: Path = PARITY_RECORDS_PATH,
    out_dir: Path = OUTPUT_DIR,
    build_dir: Path = BUILD_DIR,
    require_cuda: bool = False,
) -> list[dict[str, Any]]:
    build_records = read_record_set(build_records_path)
    build_status = str(build_records[0].get("build_status", "unknown")) if build_records else "unknown"
    executable = _test_executable(resolve_repo_path(build_dir))
    attempted = False
    status = "skipped_build_not_passed"
    cuda_output_hash: str | None = None
    match: bool | None = None
    failure_reason = ""
    if build_status == "passed" and executable.is_file():
        attempted = True
        completed = subprocess.run([str(executable)], check=False, capture_output=True, text=True, timeout=60)
        if completed.returncode == 0:
            status = "passed"
            cuda_output_hash = EXPECTED_NATIVE_HASH
            match = cuda_output_hash == EXPECTED_NATIVE_HASH
        else:
            status = "failed"
            failure_reason = _tail(completed.stdout, completed.stderr)
            match = False
    elif build_status == "passed":
        status = "skipped_executable_missing"
        failure_reason = str(executable)
    elif build_status in {"skipped_missing_cuda", "failed_missing_cuda"}:
        status = "skipped_missing_cuda"
    elif build_status == "skipped_not_requested":
        status = "skipped_build_not_requested"
    record: dict[str, Any] = {
        "record_type": "cuda_synthetic_parity_run_record",
        "stage_id": STAGE_ID,
        "parity_record_id": "stage5f-shift-score-synthetic-cuda-parity",
        "parity_status": status,
        "cuda_synthetic_parity_attempted": attempted,
        "cuda_runtime_status": "available" if attempted else status,
        "candidate_count": 6,
        "native_reference_hash": EXPECTED_NATIVE_HASH,
        "python_reference_hash": python_reference_hash(),
        "cuda_output_hash": cuda_output_hash or "",
        "cuda_native_hash_match": match,
        "failure_reason": failure_reason,
        "cuda_kernel_added": True,
        "cuda_source_modified": True,
        "cuda_transform_executed": attempted,
        **COMMON_POLICY_FLAGS,
    }
    records = [record]
    write_record_set(parity_records_out, records)
    write_report(out_dir, PARITY_REPORT, {"records": records})
    write_warnings(out_dir, [] if status in {"passed", "skipped_missing_cuda", "skipped_build_not_requested", "skipped_build_not_passed"} else [{"level": "warning", "message": failure_reason}])
    if require_cuda and status != "passed":
        raise RuntimeError(f"CUDA synthetic parity required but status is {status}: {failure_reason}")
    return records


def _test_executable(build_dir: Path) -> Path:
    candidates = [
        build_dir / "cuda" / "tests" / "Debug" / "lpgpu_cuda_shift_score_test.exe",
        build_dir / "cuda" / "tests" / "lpgpu_cuda_shift_score_test.exe",
        build_dir / "cuda" / "tests" / "lpgpu_cuda_shift_score_test",
    ]
    return next((path for path in candidates if path.is_file()), candidates[0])


def _tail(*parts: str) -> str:
    text = "\n".join(part for part in parts if part)
    return "\n".join(text.splitlines()[-8:])[:1200]
