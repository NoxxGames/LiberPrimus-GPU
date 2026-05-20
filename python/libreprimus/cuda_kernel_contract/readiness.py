"""Build Stage 5E implementation-readiness records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import resolve_repo_path
from libreprimus.cuda_kernel_contract.export import write_records_yaml, write_report
from libreprimus.cuda_kernel_contract.loaders import load_records
from libreprimus.cuda_kernel_contract.models import (
    COMMON_GUARDRAILS,
    CONTRACT_ID,
    OUTPUT_DIR,
    READINESS_ID,
    READINESS_PATH,
    READINESS_REPORT,
    SELECTED_KERNEL_ID,
    STAGE_ID,
)


def build_implementation_readiness(
    *,
    contract_path: Path,
    native_parity_path: Path,
    out_dir: Path = OUTPUT_DIR,
    readiness_out: Path = READINESS_PATH,
) -> list[dict[str, Any]]:
    contract_records = load_records(contract_path)
    native_records = load_records(native_parity_path)
    if len(contract_records) != 1 or len(native_records) != 1:
        raise ValueError("Stage 5E readiness requires exactly one contract and one native parity adapter record")
    native = native_records[0]
    status = "ready_for_stage5f_synthetic_only_implementation"
    if native.get("native_parity_mapped") is not True or native.get("stage5d_python_native_parity") is not True:
        status = "blocked_missing_native_parity"
    record = {
        "record_type": "cuda_implementation_readiness_record",
        "stage_id": STAGE_ID,
        "readiness_id": READINESS_ID,
        "contract_id": CONTRACT_ID,
        "selected_kernel_id": SELECTED_KERNEL_ID,
        "readiness_status": status,
        "stage5f_allowed_scope": "synthetic-only CUDA parity kernel implementation for the selected shift-score contract",
        "blocked_scopes": [
            "broad_search",
            "unsolved_page_campaign",
            "gpu_benchmark",
            "speedup_claim",
            "raw_data_processing",
            "canonical_corpus_activation",
            "page_boundary_finalisation",
            "solve_claim",
        ],
        "implementation_notes": [
            "Stage 5E does not add a CUDA kernel.",
            "Stage 5F must remain synthetic-only unless a later prompt explicitly expands scope.",
            "No GPU benchmark or performance claim is authorized by this readiness record.",
        ],
        **COMMON_GUARDRAILS,
    }
    resolve_repo_path(out_dir).mkdir(parents=True, exist_ok=True)
    write_records_yaml(readiness_out, [record])
    write_report(out_dir / READINESS_REPORT, {"records": [record]})
    return [record]
