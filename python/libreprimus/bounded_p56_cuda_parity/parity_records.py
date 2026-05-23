"""Parity records for Stage 5AD bounded p56 CUDA output."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_records, write_json_report, write_records
from .models import CUDA_PARITY_PATH, CUDA_RUN_PATH, EXPECTED_OUTPUT_TOKEN_HASH, OUTPUT_DIR, REPORT_FILES, SOURCE_SYNTHETIC_HASH, base_record


def build_parity_records(
    *, cuda_run: Path = CUDA_RUN_PATH, cuda_parity_out: Path = CUDA_PARITY_PATH, out_dir: Path = OUTPUT_DIR
) -> list[dict[str, Any]]:
    run = read_records(cuda_run)[0]
    computed = run.get("computed_cuda_output_token_hash")
    status = "passed" if run.get("cuda_execution_status") == "passed" and computed == EXPECTED_OUTPUT_TOKEN_HASH else str(run.get("cuda_execution_status"))
    record = base_record(
        "bounded_p56_cuda_parity_record",
        "schemas/cuda/bounded-p56-cuda-parity-record-v0.schema.json",
        parity_record_id="stage5ad-bounded-p56-cuda-parity-v0",
        validation_vector_id=run["validation_vector_id"],
        mapping_id=run["mapping_id"],
        fixture_id=run["fixture_id"],
        candidate_id=run["candidate_id"],
        expected_output_token_hash=EXPECTED_OUTPUT_TOKEN_HASH,
        computed_cuda_output_token_hash=computed,
        cuda_kernel_formula_output_token_hash=run.get("cuda_kernel_formula_output_token_hash"),
        output_hash_algorithm=run["output_hash_algorithm"],
        parity_status=status,
        stage5x_expected_hash_match=computed == EXPECTED_OUTPUT_TOKEN_HASH,
        stage5aa_synthetic_parity_reference_hash=SOURCE_SYNTHETIC_HASH,
        stage5aa_synthetic_parity_carried_forward=True,
        stage5aa_synthetic_rerun_in_stage5ad=False,
        cuda_attempted_count=run["cuda_attempted_count"],
        cuda_pass_count=run["cuda_pass_count"],
        cuda_fail_count=run["cuda_fail_count"],
        cuda_skip_count=run["cuda_skip_count"],
        bounded_p56_cuda_executed=run["bounded_p56_cuda_executed"],
        cuda_execution_performed=run["cuda_execution_performed"],
        blockers=list(run.get("blockers", [])),
    )
    records = [record]
    write_records(cuda_parity_out, records)
    write_json_report(out_dir, REPORT_FILES["parity"], {"records": records})
    return records
