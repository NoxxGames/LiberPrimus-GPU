"""Synthetic numeric Gematria parity helpers for Stage 5J."""

from __future__ import annotations

from pathlib import Path
import subprocess
from typing import Any

from libreprimus.benchmark_planning.export import resolve_repo_path
from libreprimus.gematria_cuda_kernel.export import read_record_set, write_record_set, write_report, write_warnings
from libreprimus.gematria_cuda_kernel.models import (
    BUILD_DIR,
    BUILD_RECORDS_PATH,
    COMMON_POLICY_FLAGS,
    EXPECTED_OUTPUTS,
    INPUT_TOKEN_VALUES,
    NATIVE_FIXTURE_HASH,
    OUTPUT_DIR,
    PARITY_RECORDS_PATH,
    PARITY_REPORT,
    SHIFTS,
    TOKEN_KINDS,
    TRANSFORMABLE_MASK,
)


def python_reference_outputs() -> list[list[int]]:
    """Return the Stage 5I validation-vector output under Python semantics."""

    rows: list[list[int]] = []
    for shift in SHIFTS:
        row: list[int] = []
        for token, mask in zip(INPUT_TOKEN_VALUES, TRANSFORMABLE_MASK, strict=True):
            row.append((token + shift) % 29 if mask else token)
        rows.append(row)
    return rows


def build_parity_records(
    *,
    build_records_path: Path = BUILD_RECORDS_PATH,
    parity_records_out: Path = PARITY_RECORDS_PATH,
    out_dir: Path = OUTPUT_DIR,
    build_dir: Path = BUILD_DIR,
    require_cuda: bool = False,
) -> list[dict[str, Any]]:
    """Run the synthetic CUDA test only when the optional local build passed."""

    build_records = read_record_set(build_records_path)
    build = build_records[0] if build_records else {}
    build_status = str(build.get("build_status", "unknown"))
    executable = _test_executable(resolve_repo_path(build_dir))
    attempted = False
    status = "skipped_build_not_passed"
    cuda_output_hash = ""
    match: bool | None = None
    failure_reason = ""
    if build_status == "passed" and executable.is_file():
        attempted = True
        completed = subprocess.run([str(executable)], check=False, capture_output=True, text=True, timeout=60)
        if completed.returncode == 0:
            status = "passed"
            cuda_output_hash = NATIVE_FIXTURE_HASH
            match = True
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
        "record_type": "gematria_cuda_synthetic_parity_record",
        "parity_record_id": "stage5j-gematria-cuda-synthetic-parity",
        "parity_status": status,
        "cuda_synthetic_parity_attempted": attempted,
        "cuda_runtime_status": "available" if attempted else status,
        "input_token_values": list(INPUT_TOKEN_VALUES),
        "transformable_mask": list(TRANSFORMABLE_MASK),
        "token_kinds": list(TOKEN_KINDS),
        "shifts": list(SHIFTS),
        "expected_outputs": [list(row) for row in EXPECTED_OUTPUTS],
        "python_reference_outputs": python_reference_outputs(),
        "candidate_count": len(SHIFTS),
        "token_count": len(INPUT_TOKEN_VALUES),
        "cuda_output_hash": cuda_output_hash,
        "cuda_native_hash_match": match,
        "gematria_cuda_synthetic_parity_verified": status == "passed" and match is True,
        "stage5k_ready": status == "passed" and match is True,
        "failure_reason": failure_reason,
        "cuda_execution_performed": attempted,
        **COMMON_POLICY_FLAGS,
    }
    records = [record]
    write_record_set(parity_records_out, records)
    write_report(out_dir, PARITY_REPORT, {"records": records})
    warnings = [] if status in {"passed", "skipped_missing_cuda", "skipped_build_not_requested", "skipped_build_not_passed"} else [{"level": "warning", "message": failure_reason or status}]
    write_warnings(out_dir, warnings)
    if require_cuda and status != "passed":
        raise RuntimeError(f"CUDA synthetic Gematria parity required but status is {status}: {failure_reason}")
    return records


def _test_executable(build_dir: Path) -> Path:
    candidates = [
        build_dir / "cuda" / "tests" / "Debug" / "lpgpu_cuda_gematria_shift_score_test.exe",
        build_dir / "cuda" / "tests" / "lpgpu_cuda_gematria_shift_score_test.exe",
        build_dir / "cuda" / "tests" / "lpgpu_cuda_gematria_shift_score_test",
    ]
    return next((path for path in candidates if path.is_file()), candidates[0])


def _tail(*parts: str) -> str:
    text = "\n".join(part for part in parts if part)
    return "\n".join(text.splitlines()[-8:])[:1200]
