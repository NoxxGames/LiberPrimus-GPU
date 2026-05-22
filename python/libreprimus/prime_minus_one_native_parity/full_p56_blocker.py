"""Full p56 blocker preservation records for Stage 5X."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_parity.export import read_records, write_json_report, write_records
from libreprimus.prime_minus_one_native_parity.models import COMMON_RECORD_FLAGS, FULL_P56_BLOCKER_PATH, FULL_P56_MAPPING_ID, OUTPUT_DIR, P56_FIXTURE_ID, REPORT_FILES, STAGE5W_SCHEDULE_PATH


def build_full_p56_blocker(
    *,
    full_p56_blocker_out: Path = FULL_P56_BLOCKER_PATH,
    out_dir: Path = OUTPUT_DIR,
    schedule_path: Path = STAGE5W_SCHEDULE_PATH,
) -> list[dict[str, Any]]:
    schedules = read_records(schedule_path)
    full_schedule = next(record for record in schedules if record.get("schedule_id") == "stage5w-p56-full-reference-prime-minus-one-schedule-v0")
    records = [
        {
            **COMMON_RECORD_FLAGS,
            "record_type": "prime_minus_one_full_p56_blocker_record",
            "schema": "schemas/cuda/prime-minus-one-full-p56-blocker-record-v0.schema.json",
            "blocker_id": "stage5x-full-p56-token-buffer-blocker-v0",
            "fixture_id": P56_FIXTURE_ID,
            "blocked_mapping_id": FULL_P56_MAPPING_ID,
            "blocked_schedule_id": full_schedule["schedule_id"],
            "blocker_status": "enforced",
            "blocker_reason": "needs_full_committed_p56_cipher_token_buffer_before_full_fixture_native_execution",
            "full_schedule_value_count": int(full_schedule["value_count"]),
            "full_token_buffer_committed": False,
            "native_execution_allowed": False,
            "cuda_execution_allowed": False,
            "generated_body_publication_allowed": False,
            "next_required_stage": "source-backed full p56 token-buffer expansion",
        }
    ]
    write_records(full_p56_blocker_out, records)
    write_json_report(out_dir, REPORT_FILES["full_p56_blocker"], {"records": records})
    return records
