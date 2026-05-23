"""Build method-status impact records for Stage 5AC."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_cuda_synthetic_reporting.export import write_json_report, write_records
from libreprimus.prime_minus_one_cuda_synthetic_reporting.models import METHOD_STATUS_IMPACT_PATH, OUTPUT_DIR, REPORT_FILES, base_record

METHODS = (
    ("prime_minus_one_stream", "infrastructure", "Synthetic CUDA parity is correctness metadata only."),
    ("p56_prime_minus_one", "infrastructure", "Bounded p56 is preflight-ready for a future explicit parity stage only."),
    ("scored_prime_stream_hypotheses", "deferred", "Scored experiments remain manifest-gated and unexecuted."),
)


def build_method_status_impact(
    *,
    method_status_impact_out: Path = METHOD_STATUS_IMPACT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records = [
        base_record(
            "prime_minus_one_cuda_synthetic_method_status_impact_record",
            "schemas/cuda/prime-minus-one-cuda-synthetic-method-status-impact-record-v0.schema.json",
            impact_record_id=f"stage5ac-method-impact-{method_family_id}",
            method_family_id=method_family_id,
            prior_method_status=status,
            method_status_after_stage5ac=status,
            method_status_impact="no_solved_upgrade",
            method_status_upgraded=False,
            method_status_upgrade_allowed=False,
            marked_solved=False,
            rationale=rationale,
        )
        for method_family_id, status, rationale in METHODS
    ]
    write_records(method_status_impact_out, records)
    write_json_report(out_dir, REPORT_FILES["method_status"], {"records": records})
    return records
