"""Run the optional Stage 5O exact CUDA repeat verification."""

from __future__ import annotations

from pathlib import Path
import subprocess
from typing import Any

from libreprimus.benchmark_planning.export import resolve_repo_path
from libreprimus.gematria_solved_fixture_cuda.cuda_parity import (
    _configure_and_build,
    _mark_skipped,
    _record_from_completed,
    _runner_executable,
    _write_input,
)
from libreprimus.gematria_solved_fixture_cuda_repeat.export import read_record_set, write_record_set, write_report, write_warnings
from libreprimus.gematria_solved_fixture_cuda_repeat.models import BUILD_DIR, COMMON_POLICY_FLAGS, OUTPUT_DIR, REPEAT_RUN_PATH, REPEAT_RUN_REPORT


def run_repeat_verification(
    *,
    repeat_run_records: Path = REPEAT_RUN_PATH,
    repeat_run_out: Path = REPEAT_RUN_PATH,
    out_dir: Path = OUTPUT_DIR,
    build_dir: Path = BUILD_DIR,
    skip_run: bool = False,
    require_cuda: bool = False,
) -> list[dict[str, Any]]:
    records = read_record_set(repeat_run_records)
    resolved_out_dir = resolve_repo_path(out_dir)
    resolved_build_dir = resolve_repo_path(build_dir)
    warnings: list[dict[str, Any]] = []

    if skip_run:
        updated = [_normalise_repeat_record(_mark_skipped(record, "skipped_not_requested", "skipped_not_requested")) for record in records]
        _write_outputs(repeat_run_out, out_dir, updated, warnings)
        return updated

    build_status, build_reason = _configure_and_build(resolved_build_dir)
    if build_status != "passed":
        status = "skipped_missing_cuda" if build_status == "skipped_missing_cuda" else build_status
        updated = [_normalise_repeat_record(_mark_skipped(record, build_status, status, build_reason)) for record in records]
        warnings.append({"level": "warning", "message": build_reason or build_status})
        _write_outputs(repeat_run_out, out_dir, updated, warnings)
        if require_cuda:
            raise RuntimeError(f"Stage 5O CUDA repeat required but build status is {build_status}: {build_reason}")
        return updated

    executable = _runner_executable(resolved_build_dir)
    if not executable.is_file():
        updated = [_normalise_repeat_record(_mark_skipped(record, "passed", "skipped_executable_missing", str(executable))) for record in records]
        warnings.append({"level": "warning", "message": f"missing runner executable: {executable}"})
        _write_outputs(repeat_run_out, out_dir, updated, warnings)
        if require_cuda:
            raise RuntimeError(f"Stage 5O runner executable missing: {executable}")
        return updated

    updated = []
    input_dir = resolved_out_dir / "cuda_inputs"
    input_dir.mkdir(parents=True, exist_ok=True)
    for record in records:
        input_path = _write_input(record=record, input_dir=input_dir)
        completed = subprocess.run([str(executable), str(input_path)], check=False, capture_output=True, text=True, timeout=60)
        updated.append(_normalise_repeat_record(_record_from_completed(record=record, completed=completed)))
    _write_outputs(repeat_run_out, out_dir, updated, warnings)
    if require_cuda and any(record["repeat_cuda_status"] != "passed" for record in updated):
        raise RuntimeError("Stage 5O required repeat verification but at least one fixture did not pass")
    return updated


def _normalise_repeat_record(record: dict[str, Any]) -> dict[str, Any]:
    updated = dict(record)
    cuda_hash = updated.get("cuda_output_token_hash")
    native_hash = updated.get("stage5l_native_output_token_hash") or updated.get("expected_native_output_token_hash")
    stage5m_hash = updated.get("stage5m_cuda_output_token_hash")
    native_match = cuda_hash == native_hash if cuda_hash and native_hash else None
    stage5m_match = cuda_hash == stage5m_hash if cuda_hash and stage5m_hash else None
    cuda_status = str(updated.get("cuda_run_status", "pending"))
    if cuda_status == "passed" and native_match is True and stage5m_match is True:
        repeat_status = "passed"
        failure_reason = ""
    elif cuda_status.startswith("skipped"):
        repeat_status = cuda_status
        failure_reason = str(updated.get("failure_reason", ""))
    elif cuda_status == "pending":
        repeat_status = "pending"
        failure_reason = ""
    elif native_match is False or stage5m_match is False:
        repeat_status = "failed_hash_mismatch"
        failure_reason = "repeat_output_hash_mismatch"
    else:
        repeat_status = "failed_cuda_run"
        failure_reason = str(updated.get("failure_reason", "failed_cuda_run"))
    attempted = bool(updated.get("cuda_run_attempted"))
    updated.update(COMMON_POLICY_FLAGS)
    updated.update(
        {
            "stage5l_native_output_token_hash": native_hash,
            "repeat_cuda_status": repeat_status,
            "repeat_cuda_attempted": attempted,
            "repeat_cuda_execution_performed": attempted,
            "repeat_cuda_output_token_hash": cuda_hash,
            "repeat_cuda_native_hash_match": native_match,
            "repeat_cuda_stage5m_hash_match": stage5m_match,
            "repeat_cuda_output_token_values": updated.get("cuda_output_token_values", []),
            "repeat_cuda_status_codes": updated.get("cuda_status_codes", []),
            "cuda_native_hash_match": native_match,
            "failure_reason": failure_reason,
            "stage5p_ready": repeat_status == "passed",
            "cuda_execution_performed": attempted,
            "solved_fixture_cuda_used": attempted,
            "additional_cuda_execution_performed": attempted,
            "cuda_source_modified": False,
            "new_cuda_kernel_added": False,
            "new_cuda_kernels_added": 0,
            "device_kernel_arithmetic_modified": False,
        }
    )
    return updated


def _write_outputs(path: Path, out_dir: Path, records: list[dict[str, Any]], warnings: list[dict[str, Any]]) -> None:
    write_record_set(path, records)
    write_report(out_dir, REPEAT_RUN_REPORT, {"records": records})
    write_warnings(out_dir, warnings)
