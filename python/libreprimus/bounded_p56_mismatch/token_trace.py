"""Token trace for the bounded p56 mismatch investigation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import write_json_report, write_records
from .models import (
    FORMULA_OUTPUT_TOKENS,
    INPUT_TOKENS,
    OUTPUT_DIR,
    REPORT_FILES,
    STAGE5AD_COMPUTED_CUDA_HASH,
    STAGE5AD_EXPECTED_HASH,
    STAGE5L_CANDIDATE_MAJOR_LAST_OUTPUT_TOKENS,
    TOKEN_TRACE_PATH,
    base_record,
)


def build_token_trace(*, token_trace_out: Path = TOKEN_TRACE_PATH, out_dir: Path = OUTPUT_DIR) -> list[dict[str, Any]]:
    record = base_record(
        "bounded_p56_mismatch_token_trace_record",
        "schemas/cuda/bounded-p56-mismatch-token-trace-record-v0.schema.json",
        token_trace_record_id="stage5ad-fix-token-trace-bounded-p56-v0",
        token_count=2,
        transformable_token_count=2,
        separator_count=0,
        input_tokens=INPUT_TOKENS,
        formula_output_tokens=FORMULA_OUTPUT_TOKENS,
        stage5l_candidate_major_reference_last_output_tokens=STAGE5L_CANDIDATE_MAJOR_LAST_OUTPUT_TOKENS,
        stage5ad_expected_hash=STAGE5AD_EXPECTED_HASH,
        stage5ad_computed_cuda_hash=STAGE5AD_COMPUTED_CUDA_HASH,
        token_trace_status="formula_trace_matches_cuda_hash_not_stage5l_reference_hash",
        trace_interpretation="diagnostic_only",
    )
    records = [record]
    write_records(token_trace_out, records)
    write_json_report(out_dir, REPORT_FILES["token_trace"], {"records": records})
    return records
