"""Result-store preflight records for Stage 5AD."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_records, write_json_report, write_records
from .models import CUDA_PARITY_PATH, OUTPUT_DIR, REPORT_FILES, RESULT_STORE_PREFLIGHT_PATH, base_record


def build_result_store_preflight(
    *, cuda_parity: Path = CUDA_PARITY_PATH, result_store_preflight_out: Path = RESULT_STORE_PREFLIGHT_PATH, out_dir: Path = OUTPUT_DIR
) -> list[dict[str, Any]]:
    parity = read_records(cuda_parity)[0]
    status = _preflight_status(str(parity["parity_status"]))
    record = base_record(
        "bounded_p56_cuda_result_store_preflight_record",
        "schemas/cuda/bounded-p56-cuda-result-store-preflight-record-v0.schema.json",
        result_store_preflight_id="stage5ad-bounded-p56-result-store-preflight-v0",
        result_source_kind="bounded_p56_cuda_parity",
        result_store_contract="stage4p",
        compact_summary_only=True,
        output_token_hash_required=True,
        output_text_hash_policy="blocked_pending_transliteration_policy",
        expected_output_token_hash=parity["expected_output_token_hash"],
        computed_cuda_output_token_hash=parity.get("computed_cuda_output_token_hash"),
        parity_status=parity["parity_status"],
        preflight_status=status,
    )
    records = [record]
    write_records(result_store_preflight_out, records)
    write_json_report(out_dir, REPORT_FILES["result_store"], {"records": records})
    return records


def _preflight_status(parity_status: str) -> str:
    if parity_status == "passed":
        return "ready_for_stage5ae_bounded_p56_reporting_and_integration"
    if parity_status == "failed_hash_mismatch":
        return "blocked_bounded_p56_cuda_hash_mismatch"
    return "blocked_bounded_p56_cuda_not_run"
