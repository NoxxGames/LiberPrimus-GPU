"""Stage 5D native CPU record builders."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import resolve_repo_path
from libreprimus.paths import repo_root
from libreprimus.native_cpu.export import read_yaml, write_json, write_warnings, write_yaml
from libreprimus.native_cpu.models import (
    BACKEND_ID,
    CAPABILITIES_JSON,
    CAPABILITIES_PATH,
    DIAGNOSTICS_JSON,
    DIAGNOSTICS_PATH,
    FIXTURE_ID,
    NEXT_STAGE,
    OUTPUT_DIR,
    PARITY_JSON,
    PARITY_PATH,
    POLICY_FLAGS,
    SUMMARY_JSON,
    SUMMARY_PATH,
    THREADING_JSON,
    THREADING_PATH,
    WARNINGS_JSONL,
)
from libreprimus.native_cpu.runner import python_reference_run, run_native_backend


def build_capability_and_diagnostic_records(
    *,
    native_executable: Path,
    out_dir: Path = OUTPUT_DIR,
    capabilities_out: Path = CAPABILITIES_PATH,
    diagnostics_out: Path = DIAGNOSTICS_PATH,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    native_run = run_native_backend(resolve_repo_path(native_executable), threads=1)
    executable_text = _display_path(native_executable)
    capability = {
        "record_type": "native_cpu_backend_capability_record",
        "backend_id": str(native_run["backend_id"]),
        "stage_id": "stage-5d",
        "native_backend_present": True,
        "native_backend_built": True,
        "native_backend_executable": executable_text,
        "supported_thread_counts": [1, 2, 4, 8, 16],
        "fixture_id": str(native_run["fixture_id"]),
        "candidate_count": int(native_run["candidate_count"]),
        "result_count": int(native_run["result_count"]),
        "output_hash": str(native_run["output_hash"]),
        **POLICY_FLAGS,
    }
    diagnostic = {
        "record_type": "native_cpu_diagnostic_record",
        "diagnostic_record_id": "stage5d-native-smoke-diagnostic-v0",
        "stage_id": "stage-5d",
        "backend_id": str(native_run["backend_id"]),
        "fixture_id": str(native_run["fixture_id"]),
        "diagnostic_kind": "native_backend_smoke",
        "thread_count": int(native_run["thread_count"]),
        "candidate_count": int(native_run["candidate_count"]),
        "result_count": int(native_run["result_count"]),
        "output_hash": str(native_run["output_hash"]),
        "record_hash": str(native_run["record_hash"]),
        "timing_is_diagnostic_only": True,
        **POLICY_FLAGS,
    }
    capabilities = [capability]
    diagnostics = [diagnostic]
    write_yaml(capabilities_out, {"records": capabilities})
    write_yaml(diagnostics_out, {"records": diagnostics})
    write_json(resolve_repo_path(out_dir) / CAPABILITIES_JSON, {"records": capabilities})
    write_json(resolve_repo_path(out_dir) / DIAGNOSTICS_JSON, {"records": diagnostics})
    _ensure_warnings(out_dir)
    return capabilities, diagnostics


def build_threading_records(
    *,
    native_executable: Path,
    thread_counts: list[int],
    out_dir: Path = OUTPUT_DIR,
    threading_out: Path = THREADING_PATH,
) -> list[dict[str, Any]]:
    baseline = run_native_backend(resolve_repo_path(native_executable), threads=1)
    records: list[dict[str, Any]] = []
    for count in thread_counts:
        run = run_native_backend(resolve_repo_path(native_executable), threads=count)
        records.append(
            {
                "record_type": "native_cpu_threading_record",
                "threading_record_id": f"stage5d-threading-{count:02d}-threads",
                "stage_id": "stage-5d",
                "backend_id": str(run["backend_id"]),
                "fixture_id": str(run["fixture_id"]),
                "thread_count": int(run["thread_count"]),
                "baseline_thread_count": 1,
                "candidate_count": int(run["candidate_count"]),
                "result_count": int(run["result_count"]),
                "output_hash": str(run["output_hash"]),
                "record_hash": str(run["record_hash"]),
                "baseline_output_hash": str(baseline["output_hash"]),
                "matches_baseline": run["output_hash"] == baseline["output_hash"],
                "deterministic_ordering": True,
                "fixed_output_slots": True,
                "range_partitioning": True,
                **POLICY_FLAGS,
            }
        )
    write_yaml(threading_out, {"records": records})
    write_json(resolve_repo_path(out_dir) / THREADING_JSON, {"records": records})
    _ensure_warnings(out_dir)
    return records


def build_parity_records(
    *,
    native_executable: Path,
    out_dir: Path = OUTPUT_DIR,
    parity_out: Path = PARITY_PATH,
) -> list[dict[str, Any]]:
    native = run_native_backend(resolve_repo_path(native_executable), threads=1)
    reference = python_reference_run(threads=1)
    record = {
        "record_type": "native_cpu_parity_record",
        "parity_record_id": "stage5d-native-python-limited-synthetic-parity-v0",
        "stage_id": "stage-5d",
        "backend_id": str(native["backend_id"]),
        "fixture_id": str(native["fixture_id"]),
        "parity_scope": "limited_synthetic_python_reference",
        "native_output_hash": str(native["output_hash"]),
        "python_reference_hash": str(reference["output_hash"]),
        "native_record_hash": str(native["record_hash"]),
        "python_reference_record_hash": str(reference["record_hash"]),
        "parity_passed": native["output_hash"] == reference["output_hash"],
        "candidate_count": int(native["candidate_count"]),
        "result_count": int(native["result_count"]),
        "deterministic_ordering": True,
        **POLICY_FLAGS,
    }
    records = [record]
    write_yaml(parity_out, {"records": records})
    write_json(resolve_repo_path(out_dir) / PARITY_JSON, {"records": records})
    _ensure_warnings(out_dir)
    return records


def build_summary(
    *,
    capabilities_path: Path = CAPABILITIES_PATH,
    threading_path: Path = THREADING_PATH,
    parity_path: Path = PARITY_PATH,
    diagnostics_path: Path = DIAGNOSTICS_PATH,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    capabilities = list(read_yaml(capabilities_path).get("records", []))
    threading = list(read_yaml(threading_path).get("records", []))
    parity = list(read_yaml(parity_path).get("records", []))
    diagnostics = list(read_yaml(diagnostics_path).get("records", []))
    one = next(record for record in threading if int(record["thread_count"]) == 1)
    multi = next((record for record in threading if int(record["thread_count"]) > 1), one)
    summary = {
        "record_type": "stage5d_native_cpu_summary",
        "stage_id": "stage-5d",
        "status": "complete",
        "backend_id": BACKEND_ID,
        "fixture_id": FIXTURE_ID,
        "backend_capability_records": len(capabilities),
        "threading_records": len(threading),
        "parity_records": len(parity),
        "diagnostic_records": len(diagnostics),
        "thread_counts_tested": [int(record["thread_count"]) for record in threading],
        "one_thread_hash": str(one["output_hash"]),
        "multi_thread_hash": str(multi["output_hash"]),
        "one_thread_equals_multi_thread": bool(all(record.get("matches_baseline") is True for record in threading)),
        "python_native_parity": bool(all(record.get("parity_passed") is True for record in parity)),
        "native_backend_built": bool(capabilities and capabilities[0].get("native_backend_built") is True),
        "native_backend_executable": str(capabilities[0].get("native_backend_executable", "")) if capabilities else "",
        "timing_is_diagnostic_only": True,
        "next_stage": NEXT_STAGE,
        **POLICY_FLAGS,
    }
    write_yaml(summary_out, summary)
    write_json(resolve_repo_path(out_dir) / SUMMARY_JSON, summary)
    _ensure_warnings(out_dir)
    return summary


def load_summary(path: Path = SUMMARY_PATH) -> dict[str, Any]:
    return read_yaml(path)


def _ensure_warnings(out_dir: Path) -> None:
    write_warnings(resolve_repo_path(out_dir) / WARNINGS_JSONL, [])


def _display_path(path: Path) -> str:
    resolved = resolve_repo_path(path)
    try:
        return resolved.relative_to(repo_root()).as_posix()
    except ValueError:
        return str(path)
