"""Build and print Stage 5E summary records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, resolve_repo_path, write_json, write_yaml
from libreprimus.cuda_kernel_contract.loaders import load_records
from libreprimus.cuda_kernel_contract.models import COMMON_GUARDRAILS, NEXT_STAGE, OUTPUT_DIR, SUMMARY_PATH, SUMMARY_REPORT


def build_summary(
    *,
    contract_path: Path,
    adapter_selection_path: Path,
    native_parity_path: Path,
    readiness_path: Path,
    out_dir: Path = OUTPUT_DIR,
    summary_out: Path = SUMMARY_PATH,
) -> dict[str, Any]:
    contract = load_records(contract_path)[0]
    adapter = load_records(adapter_selection_path)[0]
    native = load_records(native_parity_path)[0]
    readiness = load_records(readiness_path)[0]
    summary = {
        "record_type": "stage5e_first_kernel_contract_summary",
        "stage_id": "stage-5e",
        "status": "complete",
        "selected_kernel_id": contract["selected_kernel_id"],
        "selected_target_id": contract["selected_target_id"],
        "selected_transform_family": contract["selected_transform_family"],
        "selected_adapter_family": adapter["selected_adapter_family"],
        "alternate_candidate_count": len(contract.get("alternate_candidates", [])),
        "blocked_rejected_candidate_count": len(contract.get("blocked_or_rejected_candidates", [])),
        "native_parity_mapped": bool(native.get("native_parity_mapped")),
        "one_thread_hash": native.get("stage5d_one_thread_hash"),
        "multi_thread_hash": native.get("stage5d_multi_thread_hash"),
        "python_native_parity": native.get("stage5d_python_native_parity"),
        "implementation_readiness_status": readiness["readiness_status"],
        "next_stage": NEXT_STAGE,
        **COMMON_GUARDRAILS,
    }
    resolve_repo_path(out_dir).mkdir(parents=True, exist_ok=True)
    write_yaml(summary_out, summary)
    write_json(out_dir / SUMMARY_REPORT, summary)
    return summary


def load_summary(path: Path = SUMMARY_PATH) -> dict[str, Any]:
    return read_yaml(path)
