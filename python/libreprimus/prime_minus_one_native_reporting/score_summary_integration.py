"""Build Stage 4I-compatible Stage 5Y score-summary integration records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_reporting.export import read_records, write_json_report, write_records
from libreprimus.prime_minus_one_native_reporting.models import COMMON_RECORD_FLAGS, OUTPUT_DIR, PARITY_REPORT_PATH, REPORT_FILES, SCORE_SUMMARY_INTEGRATION_PATH


def build_score_summary_integration(
    *,
    parity_report: Path = PARITY_REPORT_PATH,
    score_summary_integration_out: Path = SCORE_SUMMARY_INTEGRATION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records = []
    for report in read_records(parity_report):
        mapping_id = str(report.get("mapping_id"))
        records.append(
            {
                **COMMON_RECORD_FLAGS,
                "record_type": "prime_minus_one_native_score_summary_integration_record",
                "schema": "schemas/cuda/prime-minus-one-native-score-summary-integration-record-v0.schema.json",
                "score_integration_record_id": f"stage5y-score-summary-{mapping_id}",
                "mapping_id": mapping_id,
                "fixture_id": report.get("fixture_id"),
                "candidate_id": report.get("candidate_id"),
                "score_summary_contract": "stage4i",
                "stage4i_compatibility": "compatible",
                "confidence_label_policy": "finite_triage_only",
                "confidence_label": "positive_control_like" if report.get("hash_match") else "scoring_not_available",
                "confidence_interpretation": "triage_only",
                "score_status_policy": "not_a_solve",
                "score_status": "scored" if report.get("hash_match") else "scoring_not_available",
                "output_token_hash_required": True,
                "output_text_hash_policy": "blocked_pending_transliteration_policy",
                "performance_claim": False,
                "speedup_claim": False,
                "method_status_upgrade_allowed": False,
                "generated_body_publication_allowed": False,
                "solve_claim": False,
            }
        )
    write_records(score_summary_integration_out, records)
    write_json_report(out_dir, REPORT_FILES["score_summary"], {"records": records})
    return records
