"""Build Stage 5T candidate batch ABI gap records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_solved_family_readiness.export import write_record_set, write_report
from libreprimus.cuda_solved_family_readiness.models import BATCH_ABI_GAP_REPORT_JSON, BATCH_ABI_GAPS_PATH, COMMON_FLAGS, OUTPUT_DIR


def build_batch_abi_gaps(
    *,
    batch_abi_gaps_out: Path = BATCH_ABI_GAPS_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Record shared ABI gaps before additional CUDA contracts."""

    gaps = [
        ("token_buffer_header", "token buffers", "needs_shared_header", True, "Common token/mask/length descriptors should be stable before more kernels."),
        ("key_schedule_buffer", "key schedules", "needs_key_schedule_abi", True, "Explicit-key Vigenere needs key-token buffers and advance rules."),
        ("stream_schedule_buffer", "stream schedules", "needs_stream_schedule_abi", True, "Prime-minus-one needs stream value, start index, and advance policy surfaces."),
        ("score_vector_shape", "score vectors", "needs_score_vector_contract", True, "Future GPU scoring needs a Stage 4I-compatible vector shape."),
        ("top_k_output_shape", "top-k outputs", "needs_top_k_output_contract", True, "Future reducers need deterministic top-k output shape and tie policy."),
    ]
    records = [
        {
            "record_type": "cuda_candidate_batch_abi_gap_record",
            "batch_abi_gap_id": f"stage5t-batch-abi-gap-{index:02d}",
            "surface_id": surface_id,
            "surface_kind": surface_kind,
            "gap_status": gap_status,
            "blocking": blocking,
            "recommended_resolution": "Stage 5U unified candidate batch ABI and backend contract consolidation",
            "rationale": rationale,
            "result_store_compatibility": "requires_compact_summary_shape",
            "score_summary_compatibility": "requires_stage4i_shape",
            **COMMON_FLAGS,
        }
        for index, (surface_id, surface_kind, gap_status, blocking, rationale) in enumerate(gaps)
    ]
    write_record_set(batch_abi_gaps_out, records)
    write_report(out_dir, BATCH_ABI_GAP_REPORT_JSON, {"records": records})
    return records
