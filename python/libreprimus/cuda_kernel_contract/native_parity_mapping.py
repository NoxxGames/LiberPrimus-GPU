"""Map Stage 5D native CPU parity onto the selected Stage 5E contract."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import resolve_repo_path
from libreprimus.cuda_kernel_contract.export import write_records_yaml, write_report
from libreprimus.cuda_kernel_contract.loaders import load_mapping, load_records
from libreprimus.cuda_kernel_contract.models import (
    COMMON_GUARDRAILS,
    CONTRACT_ID,
    NATIVE_PARITY_ADAPTER_ID,
    NATIVE_PARITY_PATH,
    NATIVE_PARITY_REPORT,
    OUTPUT_DIR,
    SELECTED_ADAPTER_FAMILY,
    SELECTED_KERNEL_ID,
    STAGE5D_SUMMARY_PATH,
    STAGE_ID,
)


def build_native_parity_adapter_map(
    *,
    contract_path: Path,
    stage5d_summary_path: Path = STAGE5D_SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
    native_parity_out: Path = NATIVE_PARITY_PATH,
) -> list[dict[str, Any]]:
    contract_records = load_records(contract_path)
    if len(contract_records) != 1:
        raise ValueError("Stage 5E contract must contain exactly one selected record")
    stage5d = load_mapping(stage5d_summary_path)
    record = {
        "record_type": "cuda_native_parity_adapter_record",
        "stage_id": STAGE_ID,
        "native_parity_adapter_id": NATIVE_PARITY_ADAPTER_ID,
        "contract_id": CONTRACT_ID,
        "selected_kernel_id": SELECTED_KERNEL_ID,
        "selected_adapter_family": SELECTED_ADAPTER_FAMILY,
        "stage5d_backend_id": stage5d.get("backend_id"),
        "stage5d_fixture_id": stage5d.get("fixture_id"),
        "stage5d_one_thread_hash": stage5d.get("one_thread_hash"),
        "stage5d_multi_thread_hash": stage5d.get("multi_thread_hash"),
        "stage5d_one_thread_equals_multi_thread": stage5d.get("one_thread_equals_multi_thread"),
        "stage5d_thread_counts": stage5d.get("thread_counts_tested", []),
        "stage5d_python_native_parity": stage5d.get("python_native_parity"),
        "timing_is_diagnostic_only": stage5d.get("timing_is_diagnostic_only"),
        "native_parity_mapped": True,
        "native_reference_scope": "Stage 5D deterministic native CPU synthetic shift fixture",
        **COMMON_GUARDRAILS,
    }
    resolve_repo_path(out_dir).mkdir(parents=True, exist_ok=True)
    write_records_yaml(native_parity_out, [record])
    write_report(out_dir / NATIVE_PARITY_REPORT, {"records": [record]})
    return [record]
