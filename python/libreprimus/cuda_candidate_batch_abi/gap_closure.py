"""Build Stage 5T ABI gap closure records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_candidate_batch_abi.export import read_record_set, write_record_set, write_report
from libreprimus.cuda_candidate_batch_abi.models import (
    ABI_GAP_CLOSURE_PATH,
    COMMON_FLAGS,
    GAP_CLOSURE_REPORT_JSON,
    OUTPUT_DIR,
    STAGE5T_GAPS,
)

_CLOSURE_MAP = {
    "token_buffer_header": ("stage5u-token_buffer_header_v0", "Stage 5V native ABI conformance adapter"),
    "key_schedule_buffer": ("stage5u-vigenere-explicit-key-schedule-v0", "Stage 5V native key-schedule conformance fixtures"),
    "stream_schedule_buffer": ("stage5u-prime-minus-one-stream-schedule-v0", "Stage 5V native stream-schedule conformance fixtures"),
    "score_vector_shape": ("stage5u-score-vector-00..06", "Stage 5V score-vector shape conformance fixtures"),
    "top_k_output_shape": ("stage5u-topk-output-contract-v0", "Stage 5V deterministic top-k conformance fixtures"),
}


def build_gap_closure(
    *,
    stage5t_gaps: Path = STAGE5T_GAPS,
    gap_closure_out: Path = ABI_GAP_CLOSURE_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Map each Stage 5T ABI gap to its Stage 5U contract closure."""

    gaps = read_record_set(stage5t_gaps)
    records: list[dict[str, Any]] = []
    for index, gap in enumerate(gaps):
        surface_id = str(gap["surface_id"])
        closure_ref, next_stage = _CLOSURE_MAP.get(surface_id, ("unknown", "Stage 5V native ABI conformance adapter"))
        records.append(
            {
                "record_type": "candidate_batch_abi_gap_closure_record",
                "gap_closure_record_id": f"stage5u-gap-closure-{index:02d}",
                "stage5t_gap_id": gap["batch_abi_gap_id"],
                "surface_id": surface_id,
                "stage5t_gap_status": gap["gap_status"],
                "stage5u_closure_status": "closed_by_contract",
                "closure_record_reference": closure_ref,
                "remaining_blockers": ["native_reference_implementation_pending"],
                "implementation_pending": True,
                "next_required_stage": next_stage,
                "notes": "Stage 5U closes the planning contract but does not implement the backend surface.",
                **COMMON_FLAGS,
            }
        )
    write_record_set(gap_closure_out, records)
    write_report(out_dir, GAP_CLOSURE_REPORT_JSON, {"records": records})
    return records
