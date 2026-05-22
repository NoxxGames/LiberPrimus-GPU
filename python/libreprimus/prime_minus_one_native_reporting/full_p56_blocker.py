"""Build Stage 5Y full-p56 blocker preservation records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_reporting.export import read_records, write_json_report, write_records
from libreprimus.prime_minus_one_native_reporting.models import COMMON_RECORD_FLAGS, FULL_P56_BLOCKER_PRESERVATION_PATH, OUTPUT_DIR, REPORT_FILES, STAGE5X_FULL_P56_BLOCKER_PATH


def build_full_p56_blocker_preservation(
    *,
    stage5x_full_p56_blocker: Path = STAGE5X_FULL_P56_BLOCKER_PATH,
    full_p56_blocker_preservation_out: Path = FULL_P56_BLOCKER_PRESERVATION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    source = read_records(stage5x_full_p56_blocker)[0]
    record = {
        **COMMON_RECORD_FLAGS,
        "record_type": "prime_minus_one_full_p56_blocker_preservation_record",
        "schema": "schemas/cuda/prime-minus-one-full-p56-blocker-preservation-record-v0.schema.json",
        "blocker_preservation_record_id": "stage5y-full-p56-blocker-preservation",
        "fixture_id": "p56-an-end-prime-minus-one",
        "blocked_mapping_id": "stage5w-mapping-p56-full-fixture-blocked-v0",
        "blocked_schedule_id": "stage5w-p56-full-reference-prime-minus-one-schedule-v0",
        "full_schedule_value_count": int(source.get("full_schedule_value_count", 84)),
        "full_token_buffer_committed": False,
        "full_p56_native_execution_allowed": False,
        "full_p56_cuda_execution_allowed": False,
        "full_p56_generated_body_publication_allowed": False,
        "blocker_status": "enforced",
        "blocker_reason": "needs_full_committed_p56_cipher_token_buffer_before_full_fixture_native_execution",
        "source_blocker_record_id": source.get("blocker_record_id"),
    }
    records = [record]
    write_records(full_p56_blocker_preservation_out, records)
    write_json_report(out_dir, REPORT_FILES["full_p56_blocker"], {"records": records})
    return records
