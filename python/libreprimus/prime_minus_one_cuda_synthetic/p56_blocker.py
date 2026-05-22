"""P56 and full-p56 blockers preserved by Stage 5AA."""

from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_synthetic.export import write_json_report, write_records
from libreprimus.prime_minus_one_cuda_synthetic.models import OUTPUT_DIR, P56_BLOCKER_PATH, REPORT_FILES, base_record


def build_p56_blocker(
    *,
    p56_blocker_out: Path = P56_BLOCKER_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    records = [
        _record(
            "stage5aa-p56-bounded-cuda-blocker-v0",
            "p56_bounded_cuda_blocked_in_stage5aa",
            "Stage 5AA executes only the Stage 5Z synthetic validation vector.",
            ["future_bounded_p56_cuda_parity_preflight_required"],
        ),
        _record(
            "stage5aa-full-p56-cuda-blocker-v0",
            "blocked_full_p56_token_buffer_missing",
            "Full p56 CUDA remains blocked until a complete committed token buffer is explicitly scoped.",
            ["needs_full_committed_p56_cipher_token_buffer_before_full_fixture_cuda_execution"],
        ),
    ]
    write_records(p56_blocker_out, records)
    write_json_report(out_dir, REPORT_FILES["p56_blocker"], {"records": records})
    return records


def _record(record_id: str, status: str, rationale: str, blockers: list[str]) -> dict[str, object]:
    return base_record(
        "prime_minus_one_cuda_synthetic_p56_blocker_record",
        "schemas/cuda/prime-minus-one-cuda-synthetic-p56-blocker-record-v0.schema.json",
        blocker_record_id=record_id,
        blocker_status=status,
        rationale=rationale,
        p56_cuda_execution_performed=False,
        full_p56_cuda_execution_performed=False,
        p56_cuda_allowed=False,
        full_p56_cuda_allowed=False,
        blockers=blockers,
    )
