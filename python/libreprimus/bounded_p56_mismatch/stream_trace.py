"""Stream trace for bounded p56 prime-minus-one diagnostics."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import write_json_report, write_records
from .models import FIRST_PRIMES_USED, OUTPUT_DIR, REPORT_FILES, STREAM_SCHEDULE_REF, STREAM_TRACE_PATH, STREAM_VALUES_USED, base_record


def build_stream_trace(*, stream_trace_out: Path = STREAM_TRACE_PATH, out_dir: Path = OUTPUT_DIR) -> list[dict[str, Any]]:
    record = base_record(
        "bounded_p56_mismatch_stream_trace_record",
        "schemas/cuda/bounded-p56-mismatch-stream-trace-record-v0.schema.json",
        stream_trace_record_id="stage5ad-fix-stream-trace-bounded-p56-v0",
        stream_schedule_ref=STREAM_SCHEDULE_REF,
        prime_index_base=0,
        prime_start_index=0,
        first_n_primes=FIRST_PRIMES_USED,
        stream_values_used=STREAM_VALUES_USED,
        stream_values_mod29=STREAM_VALUES_USED,
        stream_formula="(prime_i - 1) mod 29",
        stream_advance_policy="advance_on_enciphered_transformable_rune_tokens_only",
        value_count=2,
        raw_data_required=False,
        stream_trace_status="matches_stage5w_schedule_and_stage5x_formula_trace",
    )
    records = [record]
    write_records(stream_trace_out, records)
    write_json_report(out_dir, REPORT_FILES["stream_trace"], {"records": records})
    return records
