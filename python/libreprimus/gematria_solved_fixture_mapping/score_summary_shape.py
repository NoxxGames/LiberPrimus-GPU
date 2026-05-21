"""Build Stage 5L score-summary shape records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_solved_fixture_mapping.export import write_record_set, write_report
from libreprimus.gematria_solved_fixture_mapping.models import (
    ALLOWED_CONFIDENCE_LABELS,
    COMMON_POLICY_FLAGS,
    OUTPUT_DIR,
    SCORE_SUMMARY_CONTRACT,
    SCORE_SUMMARY_SHAPE_JSON,
    SCORE_SUMMARY_SHAPE_PATH,
)


def build_score_summary_shape_records(
    *,
    score_summary_shape_out: Path = SCORE_SUMMARY_SHAPE_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Build the Stage 4I-compatible score-summary shape for future parity records."""

    record: dict[str, Any] = {
        "record_type": "gematria_solved_fixture_score_summary_shape_record",
        "score_summary_shape_record_id": "stage5l-score-summary-shape-v0",
        "score_summary_contract": SCORE_SUMMARY_CONTRACT,
        "score_interpretation": "triage_only",
        "result_source_kind": "future_cuda_solved_fixture_safe_parity",
        "score_status_values": [
            "scored",
            "scoring_not_available",
            "calibration_not_available",
            "scorer_error",
        ],
        "allowed_confidence_labels": list(ALLOWED_CONFIDENCE_LABELS),
        "confidence_labels_triage_only": True,
        "output_token_hash_required": True,
        "output_text_hash_required": False,
        "generated_outputs_remain_ignored": True,
        "confidence_label_solve_evidence_allowed": False,
        "blockers": ["need_explicit_future_stage_approval"],
        "blocker_count": 1,
        **COMMON_POLICY_FLAGS,
    }
    records = [record]
    write_record_set(score_summary_shape_out, records)
    write_report(out_dir, SCORE_SUMMARY_SHAPE_JSON, {"records": records})
    return records
