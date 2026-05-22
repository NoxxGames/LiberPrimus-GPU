"""Score-summary preflight records for Stage 5X."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_parity.export import read_records, write_json_report, write_records
from libreprimus.prime_minus_one_native_parity.models import COMMON_RECORD_FLAGS, NATIVE_PARITY_PATH, OUTPUT_DIR, REPORT_FILES, SCORE_SUMMARY_PREFLIGHT_PATH


def build_score_summary_preflight(
    *,
    native_parity: Path = NATIVE_PARITY_PATH,
    score_summary_preflight_out: Path = SCORE_SUMMARY_PREFLIGHT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records = [_score_preflight(record) for record in read_records(native_parity)]
    write_records(score_summary_preflight_out, records)
    write_json_report(out_dir, REPORT_FILES["score_summary_preflight"], {"records": records})
    return records


def _score_preflight(parity: dict[str, Any]) -> dict[str, Any]:
    ready = parity.get("parity_status") == "passed"
    return {
        **COMMON_RECORD_FLAGS,
        "record_type": "prime_minus_one_native_score_summary_preflight_record",
        "schema": "schemas/cuda/prime-minus-one-native-score-summary-preflight-record-v0.schema.json",
        "score_summary_preflight_id": f"stage5x-score-summary-{parity['mapping_id']}",
        "mapping_id": parity["mapping_id"],
        "fixture_id": parity["fixture_id"],
        "candidate_id": parity.get("candidate_id"),
        "score_summary_contract": "stage4i",
        "stage4i_compatible": True,
        "score_interpretation": "triage_only",
        "confidence_label": "known_control" if ready else "scoring_not_available",
        "score_status": "scored" if ready else "scoring_not_available",
        "output_token_hash": parity.get("computed_output_token_hash"),
        "output_token_hash_required": True,
        "generated_body_publication_allowed": False,
        "method_status_upgrade_allowed": False,
        "solve_claim": False,
        "preflight_status": "ready_for_stage5y_compact_summary_integration" if ready else "blocked_full_p56_token_buffer_missing",
        "blockers": list(parity.get("blockers", [])),
    }
