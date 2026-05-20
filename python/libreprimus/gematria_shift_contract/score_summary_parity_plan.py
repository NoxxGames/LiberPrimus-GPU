"""Score-summary parity plan records for future Gematria CUDA outputs."""

from __future__ import annotations

from pathlib import Path

from libreprimus.gematria_shift_contract.export import write_record_set, write_report, write_warnings
from libreprimus.gematria_shift_contract.models import COMMON_POLICY_FLAGS, OUTPUT_DIR, SCORE_PLAN_ID, SCORE_PLAN_JSON, SCORE_PLAN_PATH


STAGE4I_LABELS = (
    "positive_control_like",
    "strong_lead",
    "moderate_lead",
    "weak_lead",
    "low_signal",
    "noise_like",
    "negative_control_like",
    "scoring_not_available",
    "calibration_not_available",
)


def build_score_summary_parity_plan_records(
    *,
    score_summary_plan_out: Path = SCORE_PLAN_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    """Build score-summary parity planning records."""

    record: dict[str, object] = {
        "record_type": "gematria_score_summary_parity_plan_record",
        "plan_id": SCORE_PLAN_ID,
        "score_summary_parity_plan_records": 1,
        "required_output_token_hash": True,
        "output_text_hash_policy": "optional_after_transliteration_policy_exists",
        "score_summary_status_required": True,
        "score_status_values": ["scored", "scoring_not_available", "calibration_not_available", "scorer_error"],
        "allowed_confidence_labels": list(STAGE4I_LABELS),
        "confidence_labels_triage_only": True,
        "linked_stage_records": [
            "data/scoring/stage4i-scoring-consolidation-summary.yaml",
            "data/research/stage4p-result-store-score-summary-unification-summary.yaml",
            "data/research/stage4o-cpu-batch-adapter-expansion-summary.yaml",
            "data/native-cpu/stage5d-native-cpu-summary.yaml",
            "data/cuda/stage5f-cuda-synthetic-parity-records.yaml",
            "data/cuda/stage5g-cuda-device-code-subset-audit.yaml",
        ],
        **COMMON_POLICY_FLAGS,
    }
    records = [record]
    write_record_set(score_summary_plan_out, records)
    write_report(out_dir, SCORE_PLAN_JSON, {"records": records})
    write_warnings(out_dir, [])
    return records
