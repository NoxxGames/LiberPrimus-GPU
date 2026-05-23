"""Full-p56 blocker records for Stage 5AD."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import write_json_report, write_records
from .models import FIXTURE_ID, FULL_P56_BLOCKER_PATH, OUTPUT_DIR, REPORT_FILES, base_record


def build_full_p56_blocker(
    *, full_p56_blocker_out: Path = FULL_P56_BLOCKER_PATH, out_dir: Path = OUTPUT_DIR
) -> list[dict[str, Any]]:
    record = base_record(
        "bounded_p56_cuda_full_p56_blocker_record",
        "schemas/cuda/bounded-p56-cuda-full-p56-blocker-record-v0.schema.json",
        full_p56_blocker_id="stage5ad-full-p56-blocker-v0",
        fixture_id=FIXTURE_ID,
        blocked_mapping_id="stage5w-mapping-p56-full-fixture-blocked-v0",
        blocked_schedule_id="stage5w-p56-full-reference-prime-minus-one-schedule-v0",
        full_schedule_value_count=84,
        full_token_buffer_committed=False,
        full_p56_native_execution_allowed=False,
        full_p56_cuda_execution_allowed=False,
        full_p56_generated_body_publication_allowed=False,
        blocker_status="enforced",
        full_p56_status="blocked_full_p56_token_buffer_missing",
        blocker_reason="needs_full_committed_p56_cipher_token_buffer_before_full_fixture_cuda_execution",
    )
    records = [record]
    write_records(full_p56_blocker_out, records)
    write_json_report(out_dir, REPORT_FILES["full_p56"], {"records": records})
    return records
