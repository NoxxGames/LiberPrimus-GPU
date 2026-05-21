"""Build Stage 5O score-summary preflight records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_solved_fixture_cuda_repeat.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_solved_fixture_cuda_repeat.models import COMMON_POLICY_FLAGS, OUTPUT_DIR, REPEAT_PARITY_PATH, SCORE_SUMMARY_CONTRACT, SCORE_SUMMARY_PREFLIGHT_PATH, SCORE_SUMMARY_PREFLIGHT_REPORT


def build_score_summary_preflight(
    *,
    repeat_parity: Path = REPEAT_PARITY_PATH,
    score_summary_preflight_out: Path = SCORE_SUMMARY_PREFLIGHT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    parity = read_record_set(repeat_parity)
    pass_count = sum(1 for record in parity if record["repeat_parity_status"] == "passed")
    ready = pass_count == 5
    record = {
        "record_type": "stage5o_gematria_cuda_score_summary_preflight_record",
        "score_summary_preflight_id": "stage5o-score-summary-preflight-00",
        "score_summary_contract": SCORE_SUMMARY_CONTRACT,
        "score_interpretation": "triage_only",
        "stage4i_confidence_labels_only": True,
        "new_scorer_added": False,
        "score_summary_shape_status": "ready_for_stage5p_compact_summary_integration" if ready else "blocked_repeat_parity_not_clean",
        "repeat_parity_pass_count": pass_count,
        "expected_repeat_parity_pass_count": 5,
        "confidence_label": "scoring_not_available",
        "score_status": "scoring_not_available",
        "output_token_hashes_available": pass_count,
        "stage5p_ready": ready,
        "cuda_execution_performed": False,
        "solved_fixture_cuda_used": False,
        "additional_cuda_execution_performed": False,
    }
    record.update(COMMON_POLICY_FLAGS)
    records = [record]
    write_record_set(score_summary_preflight_out, records)
    write_report(out_dir, SCORE_SUMMARY_PREFLIGHT_REPORT, {"records": records})
    return records
