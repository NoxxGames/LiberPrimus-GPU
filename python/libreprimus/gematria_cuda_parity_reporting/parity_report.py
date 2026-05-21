"""Stage 5K Gematria CUDA parity report generation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml
from libreprimus.gematria_cuda_parity_reporting.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_cuda_parity_reporting.models import (
    COMMON_POLICY_FLAGS,
    NATIVE_FIXTURE_HASH,
    OUTPUT_DIR,
    PARITY_REPORT_JSON,
    PARITY_REPORT_PATH,
    SOURCE_CONTRACT_ID,
    STAGE5J_PARITY_PATH,
    STAGE5J_SUMMARY_PATH,
)


def build_parity_report(
    *,
    stage5j_summary_path: Path = STAGE5J_SUMMARY_PATH,
    stage5j_parity_path: Path = STAGE5J_PARITY_PATH,
    parity_report_out: Path = PARITY_REPORT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    summary = read_yaml(stage5j_summary_path)
    parity_records = read_record_set(stage5j_parity_path)
    parity = parity_records[0] if parity_records else {}
    cuda_hash = str(parity.get("cuda_output_hash") or summary.get("cuda_output_hash") or "")
    hash_match = bool(parity.get("cuda_native_hash_match") is True and cuda_hash == NATIVE_FIXTURE_HASH)
    record: dict[str, Any] = {
        "record_type": "gematria_cuda_parity_report_record",
        "parity_report_id": "stage5k-gematria-stage5j-parity-report",
        "stage5j_summary_path": str(stage5j_summary_path),
        "stage5j_parity_path": str(stage5j_parity_path),
        "stage5j_cuda_build_status": str(summary.get("cuda_build_status", "unknown")),
        "stage5j_cuda_synthetic_parity_status": str(summary.get("cuda_synthetic_parity_status", "unknown")),
        "cuda_output_hash": cuda_hash,
        "cuda_native_hash_match": hash_match,
        "gematria_cuda_synthetic_parity_verified": hash_match,
        "source_contract_id_verified": summary.get("source_contract_id") == SOURCE_CONTRACT_ID,
        "native_fixture_hash_verified": summary.get("native_fixture_hash") == NATIVE_FIXTURE_HASH,
        "current_kernel_scope": "synthetic_numeric_gematria_mod29_only",
        "stage5k_reporting_only": True,
        "notes": [
            "Stage 5K reports the Stage 5J synthetic Gematria CUDA/native hash match only.",
            "The Stage 5J synthetic numeric parity pass does not authorize solved-fixture or real LP CUDA execution.",
        ],
        **COMMON_POLICY_FLAGS,
    }
    records = [record]
    write_record_set(parity_report_out, records)
    write_report(out_dir, PARITY_REPORT_JSON, {"records": records})
    return records
