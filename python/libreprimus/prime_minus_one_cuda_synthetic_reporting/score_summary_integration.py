"""Build Stage 4I-compatible score-summary integration records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_cuda_synthetic_reporting.export import read_records, write_json_report, write_records
from libreprimus.prime_minus_one_cuda_synthetic_reporting.models import OUTPUT_DIR, PARITY_REPORT_PATH, REPORT_FILES, SCORE_SUMMARY_INTEGRATION_PATH, base_record


def build_score_summary_integration(
    *,
    parity_report: Path = PARITY_REPORT_PATH,
    score_summary_integration_out: Path = SCORE_SUMMARY_INTEGRATION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    report = read_records(parity_report)[0]
    records = [
        base_record(
            "prime_minus_one_cuda_synthetic_score_summary_integration_record",
            "schemas/cuda/prime-minus-one-cuda-synthetic-score-summary-integration-record-v0.schema.json",
            integration_record_id="stage5ac-score-summary-synthetic-parity-v0",
            source_report_record_id=report.get("report_record_id"),
            score_summary_contract="stage4i",
            score_status="scored",
            score_interpretation="triage_only",
            confidence_label="positive_control_like",
            score_summary_shape="hash_parity_metadata_only",
            score_summary_available=True,
            score_components=[],
            calibration_profile="stage4i-positive-control-fixture-profile",
            parity_status=report.get("parity_status"),
            output_token_hash=report.get("computed_output_token_hash"),
            scoring_model_added=False,
            scorer_semantics_changed=False,
        )
    ]
    write_records(score_summary_integration_out, records)
    write_json_report(out_dir, REPORT_FILES["score_summary"], {"records": records})
    return records
