"""Build compact Stage 5AC synthetic CUDA parity report records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_cuda_synthetic_reporting.export import read_records, read_yaml, write_json_report, write_records
from libreprimus.prime_minus_one_cuda_synthetic_reporting.models import (
    EXPECTED_SYNTHETIC_HASH,
    HASH_ALGORITHM,
    OUTPUT_DIR,
    PARITY_REPORT_PATH,
    REPORT_FILES,
    STAGE5AA_PARITY_PATH,
    STAGE5AA_SUMMARY_PATH,
    SYNTHETIC_MAPPING_ID,
    SYNTHETIC_VECTOR_ID,
    base_record,
)


def build_parity_report(
    *,
    stage5aa_summary: Path = STAGE5AA_SUMMARY_PATH,
    stage5aa_parity: Path = STAGE5AA_PARITY_PATH,
    parity_report_out: Path = PARITY_REPORT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    summary = read_yaml(stage5aa_summary)
    source = read_records(stage5aa_parity)[0]
    expected = str(summary.get("expected_output_token_hash") or source.get("expected_output_token_hash"))
    computed = str(summary.get("computed_output_token_hash") or source.get("computed_output_token_hash"))
    records = [
        base_record(
            "prime_minus_one_cuda_synthetic_parity_report_record",
            "schemas/cuda/prime-minus-one-cuda-synthetic-parity-report-record-v0.schema.json",
            report_record_id="stage5ac-synthetic-parity-report-v0",
            synthetic_vector_id=SYNTHETIC_VECTOR_ID,
            mapping_id=SYNTHETIC_MAPPING_ID,
            source_parity_record_id=source.get("parity_record_id"),
            expected_output_token_hash=expected,
            computed_output_token_hash=computed,
            output_hash_algorithm=HASH_ALGORITHM,
            parity_status=summary.get("parity_status"),
            stage5aa_hash_match=expected == computed == EXPECTED_SYNTHETIC_HASH,
            source_stage5aa_cuda_attempted=bool(summary.get("cuda_attempted")),
            source_stage5aa_cuda_execution_performed=bool(source.get("cuda_execution_performed")),
            source_stage5aa_cuda_pass_count=int(summary.get("cuda_pass_count", 0)),
            source_stage5aa_cuda_fail_count=int(summary.get("cuda_fail_count", 0)),
            source_stage5aa_cuda_skip_count=int(summary.get("cuda_skip_count", 0)),
            source_stage5aa_cuda_source_modified=bool(summary.get("cuda_source_modified")),
            source_stage5aa_new_cuda_kernels_added=int(summary.get("new_cuda_kernels_added", 0)),
            cuda_execution_performed_in_stage5ac=False,
            cuda_source_modified_in_stage5ac=False,
            new_cuda_kernels_added_in_stage5ac=0,
            blockers=[],
        )
    ]
    write_records(parity_report_out, records)
    write_json_report(out_dir, REPORT_FILES["parity"], {"records": records})
    return records
