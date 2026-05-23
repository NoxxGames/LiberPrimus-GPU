"""Preserve full-p56 blocker records for Stage 5AC."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_cuda_synthetic_reporting.export import write_json_report, write_records
from libreprimus.prime_minus_one_cuda_synthetic_reporting.models import FULL_P56_BLOCKER_PATH, OUTPUT_DIR, REPORT_FILES, base_record


def build_full_p56_blocker(
    *,
    full_p56_blocker_out: Path = FULL_P56_BLOCKER_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records = [
        base_record(
            "prime_minus_one_cuda_synthetic_full_p56_blocker_record",
            "schemas/cuda/prime-minus-one-cuda-synthetic-full-p56-blocker-record-v0.schema.json",
            blocker_record_id="stage5ac-full-p56-blocker-v0",
            full_p56_status="blocked_full_p56_token_buffer_missing",
            full_p56_cuda_execution_allowed=False,
            full_p56_native_execution_allowed=False,
            full_p56_generated_body_publication_allowed=False,
            blocker_reason="needs_full_committed_p56_cipher_token_buffer_before_full_fixture_cuda_execution",
            full_p56_token_buffer_committed=False,
            full_p56_required_for_stage5ad=False,
        )
    ]
    write_records(full_p56_blocker_out, records)
    write_json_report(out_dir, REPORT_FILES["full_p56"], {"records": records})
    return records
