"""Build Stage 5Z full-p56 blocker preservation records."""

from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_contract.export import write_json_report, write_records
from libreprimus.prime_minus_one_cuda_contract.models import FULL_P56_BLOCKER_PATH, FULL_P56_MAPPING_ID, OUTPUT_DIR, base_record


def build_full_p56_blocker(
    full_p56_blocker_out: Path = FULL_P56_BLOCKER_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict]:
    record = base_record(
        "prime_minus_one_cuda_full_p56_blocker_record",
        "schemas/cuda/prime-minus-one-cuda-full-p56-blocker-record-v0.schema.json",
        blocker_record_id="stage5z-full-p56-blocker-v0",
        mapping_id=FULL_P56_MAPPING_ID,
        blocker_status="enforced",
        full_p56_status="blocked_full_p56_token_buffer_missing",
        full_token_buffer_committed=False,
        full_schedule_value_count=84,
        required_before_unblock=[
            "committed_full_p56_cipher_token_buffer",
            "reviewed_fixture_boundary_policy",
            "explicit_future_stage_authorization",
            "no_unsolved_page_scope_guardrail",
        ],
        cuda_execution_allowed=False,
        full_p56_cuda_allowed=False,
    )
    records = [record]
    write_records(full_p56_blocker_out, records)
    write_json_report(out_dir, "full_p56_blocker_report.json", {"records": records})
    return records


__all__ = ["build_full_p56_blocker"]
