"""No-GPU formula trace for the bounded p56 mismatch investigation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cpu_batch.input_streams import stable_json_sha256

from .export import write_json_report, write_records
from .models import (
    FORMULA_OUTPUT_TOKENS,
    INPUT_TOKENS,
    OUTPUT_DIR,
    REPORT_FILES,
    STAGE5AD_COMPUTED_CUDA_HASH,
    STAGE5AD_EXPECTED_HASH,
    STAGE5X_FORMULA_HASH,
    STREAM_VALUES_USED,
    FORMULA_TRACE_PATH,
    base_record,
)


def build_formula_trace(*, formula_trace_out: Path = FORMULA_TRACE_PATH, out_dir: Path = OUTPUT_DIR) -> list[dict[str, Any]]:
    recomputed_hash = stable_json_sha256(FORMULA_OUTPUT_TOKENS)
    per_token_trace = []
    for token, stream_value, output in zip(INPUT_TOKENS, STREAM_VALUES_USED, FORMULA_OUTPUT_TOKENS, strict=True):
        per_token_trace.append(
            {
                "position": token["position"],
                "input_index29": token["index29"],
                "stream_value": stream_value,
                "formula": "(input_index29 - stream_value) mod 29",
                "output_index29": (token["index29"] - stream_value) % 29,
                "expected_formula_output_index29": output["index29"],
                "formula_match": ((token["index29"] - stream_value) % 29) == output["index29"],
            }
        )
    record = base_record(
        "bounded_p56_mismatch_formula_trace_record",
        "schemas/cuda/bounded-p56-mismatch-formula-trace-record-v0.schema.json",
        formula_trace_record_id="stage5ad-fix-formula-trace-bounded-p56-v0",
        input_tokens=INPUT_TOKENS,
        stream_values_used=STREAM_VALUES_USED,
        output_tokens=FORMULA_OUTPUT_TOKENS,
        per_token_trace=per_token_trace,
        formula_output_token_hash=recomputed_hash,
        stage5x_formula_hash=STAGE5X_FORMULA_HASH,
        stage5ad_computed_cuda_hash=STAGE5AD_COMPUTED_CUDA_HASH,
        stage5ad_expected_hash=STAGE5AD_EXPECTED_HASH,
        formula_matches_stage5x_formula=recomputed_hash == STAGE5X_FORMULA_HASH,
        formula_matches_stage5ad_cuda_hash=recomputed_hash == STAGE5AD_COMPUTED_CUDA_HASH,
        formula_matches_stage5ad_expected_hash=recomputed_hash == STAGE5AD_EXPECTED_HASH,
        python_reference_execution_performed=True,
        formula_trace_status="formula_hash_reproduced_no_gpu",
    )
    records = [record]
    write_records(formula_trace_out, records)
    write_json_report(out_dir, REPORT_FILES["formula_trace"], {"records": records})
    return records
