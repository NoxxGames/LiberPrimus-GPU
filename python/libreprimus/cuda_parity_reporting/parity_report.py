"""Stage 5G shift_score parity-report record generation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml
from libreprimus.cuda_parity_reporting.export import read_record_set, write_record_set, write_report
from libreprimus.cuda_parity_reporting.models import (
    COMMON_POLICY_FLAGS,
    NATIVE_REFERENCE_HASH,
    OUTPUT_DIR,
    PARITY_REPORT_JSON,
    PARITY_REPORT_PATH,
    STAGE5F_PARITY_PATH,
    STAGE5F_SUMMARY_PATH,
    STAGE_ID,
)


def build_parity_report(
    *,
    stage5f_summary_path: Path = STAGE5F_SUMMARY_PATH,
    stage5f_parity_path: Path = STAGE5F_PARITY_PATH,
    parity_report_out: Path = PARITY_REPORT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    summary = read_yaml(stage5f_summary_path)
    parity_records = read_record_set(stage5f_parity_path)
    parity = parity_records[0] if parity_records else {}
    cuda_hash = str(parity.get("cuda_output_hash") or summary.get("cuda_output_hash") or "")
    record: dict[str, Any] = {
        "record_type": "cuda_shift_score_parity_report_record",
        "stage_id": STAGE_ID,
        "parity_report_id": "stage5g-shift-score-stage5f-parity-report",
        "stage5f_summary_path": str(stage5f_summary_path),
        "stage5f_parity_path": str(stage5f_parity_path),
        "stage5f_cuda_build_status": str(summary.get("cuda_build_status", "unknown")),
        "stage5f_cuda_synthetic_parity_status": str(summary.get("cuda_synthetic_parity_status", "unknown")),
        "native_reference_hash": NATIVE_REFERENCE_HASH,
        "stage5f_cuda_output_hash": cuda_hash,
        "stage5f_cuda_native_hash_match": bool(parity.get("cuda_native_hash_match") is True and cuda_hash == NATIVE_REFERENCE_HASH),
        "current_kernel_scope": "synthetic_uppercase_latin_a_to_z_only",
        "production_gematria_mod29_cuda_ready": False,
        "solved_fixture_cuda_execution_allowed": False,
        "cuda_source_modified": True,
        "notes": [
            "Stage 5G reports the Stage 5F synthetic CUDA/native hash match only.",
            "The Stage 5F kernel remains uppercase Latin synthetic parity, not production Gematria mod-29 CUDA.",
        ],
        **COMMON_POLICY_FLAGS,
    }
    records = [record]
    write_record_set(parity_report_out, records)
    write_report(out_dir, PARITY_REPORT_JSON, {"records": records})
    return records
