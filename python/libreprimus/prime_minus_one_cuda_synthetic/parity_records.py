"""Stage 5AA synthetic CUDA parity records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_cuda_synthetic.export import read_records, write_json_report, write_records
from libreprimus.prime_minus_one_cuda_synthetic.models import (
    CUDA_RUN_PATH,
    EXPECTED_SYNTHETIC_HASH,
    HASH_ALGORITHM,
    OUTPUT_DIR,
    PARITY_PATH,
    REPORT_FILES,
    SYNTHETIC_FIXTURE_ID,
    SYNTHETIC_MAPPING_ID,
    VALIDATION_VECTOR_ID,
    base_record,
)


def build_parity_records(
    *,
    cuda_run: Path = CUDA_RUN_PATH,
    parity_out: Path = PARITY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    run = read_records(cuda_run)[0]
    computed_hash = run.get("computed_output_token_hash")
    if computed_hash == EXPECTED_SYNTHETIC_HASH and run.get("cuda_run_status") == "passed":
        parity_status = "passed"
        blockers: list[str] = []
    elif computed_hash and computed_hash != EXPECTED_SYNTHETIC_HASH:
        parity_status = "failed_hash_mismatch"
        blockers = ["cuda_hash_mismatch"]
    elif run.get("cuda_attempted") is True:
        parity_status = "failed_cuda_run"
        blockers = list(run.get("blockers", [])) or ["cuda_run_failed"]
    else:
        parity_status = "skipped_cuda_unavailable"
        blockers = list(run.get("blockers", [])) or ["cuda_run_skipped"]
    record = base_record(
        "prime_minus_one_cuda_synthetic_parity_record",
        "schemas/cuda/prime-minus-one-cuda-synthetic-parity-record-v0.schema.json",
        parity_record_id="stage5aa-prime-minus-one-cuda-synthetic-parity-v0",
        run_record_id=run.get("run_record_id"),
        validation_vector_id=VALIDATION_VECTOR_ID,
        mapping_id=SYNTHETIC_MAPPING_ID,
        fixture_id=SYNTHETIC_FIXTURE_ID,
        expected_output_token_hash=EXPECTED_SYNTHETIC_HASH,
        computed_output_token_hash=computed_hash,
        output_hash_algorithm=HASH_ALGORITHM,
        parity_status=parity_status,
        expected_hash_match=computed_hash == EXPECTED_SYNTHETIC_HASH,
        stage5z_validation_vector_matched=computed_hash == EXPECTED_SYNTHETIC_HASH,
        cuda_execution_performed=bool(run.get("cuda_attempted")),
        cuda_pass_count=int(run.get("cuda_pass_count", 0)),
        cuda_fail_count=int(run.get("cuda_fail_count", 0)),
        cuda_skip_count=int(run.get("cuda_skip_count", 0)),
        p56_cuda_execution_performed=False,
        full_p56_cuda_execution_performed=False,
        unsolved_page_cuda_used=False,
        scored_experiment_executed=False,
        blockers=blockers,
    )
    records = [record]
    write_records(parity_out, records)
    write_json_report(out_dir, REPORT_FILES["parity"], {"records": records})
    return records
