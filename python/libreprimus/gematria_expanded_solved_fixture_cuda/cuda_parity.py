"""Optional local CUDA execution for Stage 5R expanded solved-fixture parity."""

from __future__ import annotations

from pathlib import Path
import os
import shutil
import subprocess
from typing import Any

from libreprimus.benchmark_planning.export import resolve_repo_path
from libreprimus.gematria_expanded_solved_fixture_cuda.export import read_record_set, write_record_set, write_report, write_warnings
from libreprimus.gematria_expanded_solved_fixture_cuda.models import (
    BUILD_DIR,
    OUTPUT_DIR,
    OUTPUT_ORDERING,
    RUN_RECORDS_PATH,
    RUN_REPORT,
    TOKEN_DOMAIN,
)
from libreprimus.gematria_expansion_candidate_mapping.token_mapping import canonical_hash
from libreprimus.paths import repo_root


def run_cuda_parity(
    *,
    run_records_path: Path = RUN_RECORDS_PATH,
    run_records_out: Path = RUN_RECORDS_PATH,
    out_dir: Path = OUTPUT_DIR,
    build_dir: Path = BUILD_DIR,
    skip_run: bool = False,
    require_cuda: bool = False,
) -> list[dict[str, Any]]:
    records = read_record_set(run_records_path)
    out_dir = resolve_repo_path(out_dir)
    build_dir = resolve_repo_path(build_dir)
    warnings: list[dict[str, Any]] = []

    if skip_run:
        updated = [_mark_skipped(record, "skipped_not_requested", "skipped_not_requested") for record in records]
        _write_outputs(run_records_out, out_dir, updated, warnings)
        return updated

    build_status, build_reason = _configure_and_build(build_dir)
    if build_status != "passed":
        status = "skipped_missing_cuda" if build_status == "skipped_missing_cuda" else build_status
        updated = [_mark_skipped(record, build_status, status, build_reason) for record in records]
        warnings.append({"level": "warning", "message": build_reason or build_status})
        _write_outputs(run_records_out, out_dir, updated, warnings)
        if require_cuda:
            raise RuntimeError(f"Stage 5R CUDA run required but build status is {build_status}: {build_reason}")
        return updated

    executable = _runner_executable(build_dir)
    if not executable.is_file():
        updated = [_mark_skipped(record, "passed", "skipped_executable_missing", str(executable)) for record in records]
        _write_outputs(run_records_out, out_dir, updated, [{"level": "warning", "message": f"missing runner executable: {executable}"}])
        if require_cuda:
            raise RuntimeError(f"Stage 5R runner executable missing: {executable}")
        return updated

    updated = []
    input_dir = out_dir / "cuda_inputs"
    input_dir.mkdir(parents=True, exist_ok=True)
    for record in records:
        input_path = _write_input(record=record, input_dir=input_dir)
        completed = subprocess.run([str(executable), str(input_path)], check=False, capture_output=True, text=True, timeout=60)
        updated.append(_record_from_completed(record=record, completed=completed))
    _write_outputs(run_records_out, out_dir, updated, warnings)
    if require_cuda and any(record["cuda_run_status"] != "passed" for record in updated):
        raise RuntimeError("Stage 5R required CUDA parity but at least one fixture did not pass")
    return updated


def _configure_and_build(build_dir: Path) -> tuple[str, str]:
    cmake_path = shutil.which("cmake")
    nvcc_path = _find_nvcc()
    if cmake_path is None or nvcc_path is None:
        return "skipped_missing_cuda", "cmake_or_nvcc_missing"

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
    if os.name == "nt":
        toolkit_root = _toolkit_root(nvcc_path)
        if toolkit_root is not None:
            configure_command[1:1] = ["-T", f"cuda={toolkit_root}"]
    else:
        configure_command.append(f"-DCMAKE_CUDA_COMPILER={nvcc_path}")
    configure = subprocess.run(configure_command, check=False, capture_output=True, text=True, timeout=180)
    if configure.returncode != 0:
        failure = _tail(configure.stdout, configure.stderr)
        return _classify_configure_failure(failure), failure
    build = subprocess.run(
        ["cmake", "--build", str(build_dir), "--target", "lpgpu_cuda_gematria_shift_score_stage5m_runner", "--config", "Debug"],
        check=False,
        capture_output=True,
        text=True,
        timeout=240,
    )
    if build.returncode != 0:
        return "failed_environment", _tail(build.stdout, build.stderr)
    return "passed", ""


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


def _classify_configure_failure(text: str) -> str:
    lowered = text.lower()
    if "could not find" in lowered and "cuda" in lowered:
        return "failed_toolkit_resolution"
    if "cuda toolkit directory" in lowered or "toolkit" in lowered:
        return "failed_toolkit_resolution"
    return "failed_environment"


def _runner_executable(build_dir: Path) -> Path:
    candidates = [
        build_dir / "cuda" / "tests" / "Debug" / "lpgpu_cuda_gematria_shift_score_stage5m_runner.exe",
        build_dir / "cuda" / "tests" / "lpgpu_cuda_gematria_shift_score_stage5m_runner.exe",
        build_dir / "cuda" / "tests" / "lpgpu_cuda_gematria_shift_score_stage5m_runner",
    ]
    return next((path for path in candidates if path.is_file()), candidates[0])


def _write_input(*, record: dict[str, Any], input_dir: Path) -> Path:
    run_id = str(record["run_record_id"]).replace("/", "_")
    path = input_dir / f"{run_id}.txt"
    token_values = [0 if value is None else int(value) for value in record["token_values"]]
    mask = [1 if value else 0 for value in record["transformable_mask"]]
    shifts = [int(value) for value in record["candidate_shifts"]]
    text = "\n".join(
        [
            f"{len(token_values)} {len(shifts)}",
            " ".join(str(value) for value in token_values),
            " ".join(str(value) for value in mask),
            " ".join(str(value) for value in shifts),
            "",
        ]
    )
    path.write_text(text, encoding="utf-8")
    return path


def _record_from_completed(*, record: dict[str, Any], completed: subprocess.CompletedProcess[str]) -> dict[str, Any]:
    updated = dict(record)
    updated["cuda_build_status"] = "passed"
    updated["cuda_run_attempted"] = True
    updated["cuda_execution_performed"] = True
    updated["solved_fixture_cuda_used"] = True
    parsed = _parse_output(completed.stdout)
    if completed.returncode != 0 or parsed.get("status") != "0":
        updated["cuda_run_status"] = "failed"
        updated["cuda_native_hash_match"] = False
        updated["failure_reason"] = _tail(completed.stdout, completed.stderr)
        updated["stage5s_ready"] = False
        return updated
    output_values = [int(value) for value in parsed.get("output_token_values", "").split(",") if value != ""]
    status_codes = [int(value) for value in parsed.get("status_codes", "").split(",") if value != ""]
    output_hash = _cuda_hash(record=record, output_values=output_values)
    native_hash = record.get("expected_native_output_token_hash")
    match = output_hash == native_hash
    updated["cuda_output_token_hash"] = output_hash
    updated["stage5r_cuda_output_token_hash"] = output_hash
    updated["cuda_output_token_values"] = output_values
    updated["cuda_status_codes"] = status_codes
    updated["cuda_native_hash_match"] = match
    updated["cuda_run_status"] = "passed" if match else "failed"
    updated["failure_reason"] = "" if match else "cuda_output_hash_mismatch"
    updated["stage5s_ready"] = match
    return updated


def _cuda_hash(*, record: dict[str, Any], output_values: list[int]) -> str:
    token_count = int(record["token_count"])
    candidate_outputs = []
    for candidate_index, shift in enumerate(record["candidate_shifts"]):
        start = candidate_index * token_count
        output_tokens = []
        for token_index, token in enumerate(record["token_records"]):
            if token["transformable"]:
                output_tokens.append(
                    {
                        "position": token["position"],
                        "token_kind": token["token_kind"],
                        "transformable": True,
                        "index29": output_values[start + token_index],
                        "raw_text": None,
                    }
                )
            else:
                output_tokens.append(
                    {
                        "position": token["position"],
                        "token_kind": token["token_kind"],
                        "transformable": False,
                        "index29": None,
                        "raw_text": token.get("raw_text"),
                    }
                )
        candidate_outputs.append({"candidate_index": candidate_index, "shift": shift, "output_tokens": output_tokens})
    return canonical_hash(
        {
            "contract_id": "stage5q-expansion-output-hash-contract-v0",
            "token_mapping_record_id": record["token_mapping_record_id"],
            "candidate_inventory_id": record["candidate_inventory_id"],
            "source_input_stream_id": record["source_input_stream_id"],
            "fixture_id": record["fixture_id"],
            "candidate_id": record["candidate_id"],
            "token_domain": TOKEN_DOMAIN,
            "candidate_ordering": OUTPUT_ORDERING,
            "candidate_outputs": candidate_outputs,
        }
    )


def _mark_skipped(record: dict[str, Any], build_status: str, run_status: str, reason: str = "") -> dict[str, Any]:
    updated = dict(record)
    updated["cuda_build_status"] = build_status
    updated["cuda_run_status"] = run_status
    updated["cuda_run_attempted"] = False
    updated["cuda_execution_performed"] = False
    updated["solved_fixture_cuda_used"] = False
    updated["cuda_native_hash_match"] = None
    updated["failure_reason"] = reason
    updated["stage5s_ready"] = False
    return updated


def _parse_output(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def _tail(*parts: str) -> str:
    text = "\n".join(part for part in parts if part)
    return "\n".join(text.splitlines()[-10:])[:1600]


def _write_outputs(path: Path, out_dir: Path, records: list[dict[str, Any]], warnings: list[dict[str, Any]]) -> None:
    write_record_set(path, records)
    write_report(out_dir, RUN_REPORT, {"records": records})
    write_warnings(out_dir, warnings)
