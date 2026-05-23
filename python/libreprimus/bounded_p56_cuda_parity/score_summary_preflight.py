"""Score-summary preflight records for Stage 5AD."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_records, write_json_report, write_records
from .models import CUDA_PARITY_PATH, OUTPUT_DIR, REPORT_FILES, SCORE_SUMMARY_PREFLIGHT_PATH, base_record
from .result_store_preflight import _preflight_status


def build_score_summary_preflight(
    *, cuda_parity: Path = CUDA_PARITY_PATH, score_summary_preflight_out: Path = SCORE_SUMMARY_PREFLIGHT_PATH, out_dir: Path = OUTPUT_DIR
) -> list[dict[str, Any]]:
    parity = read_records(cuda_parity)[0]
    record = base_record(
        "bounded_p56_cuda_score_summary_preflight_record",
        "schemas/cuda/bounded-p56-cuda-score-summary-preflight-record-v0.schema.json",
        score_summary_preflight_id="stage5ad-bounded-p56-score-summary-preflight-v0",
        score_summary_contract="stage4i",
        score_summary_label_policy="finite_triage_only",
        confidence_label="positive_control_like" if parity["parity_status"] == "passed" else "scoring_not_available",
        confidence_interpretation="triage_only",
        score_status="scored" if parity["parity_status"] == "passed" else "scoring_not_available",
        parity_status=parity["parity_status"],
        preflight_status=_preflight_status(str(parity["parity_status"])),
        method_status_upgrade_allowed=False,
        generated_body_publication_allowed=False,
        performance_claim_allowed=False,
        speedup_claim_allowed=False,
    )
    records = [record]
    write_records(score_summary_preflight_out, records)
    write_json_report(out_dir, REPORT_FILES["score_summary"], {"records": records})
    return records
