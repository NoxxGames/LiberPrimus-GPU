"""Scorer inventory for existing local scoring code."""

from __future__ import annotations

from libreprimus.scoring_consolidation.models import CALIBRATION_PROFILE_ID, SCORER_ID, SCORER_VERSION


def scorer_records() -> list[dict[str, object]]:
    """Return durable scorer inventory records without changing scorer behavior."""

    return [
        {
            "record_type": "scorer_record",
            "scorer_id": SCORER_ID,
            "scorer_version": SCORER_VERSION,
            "module": "libreprimus.scoring.minimal_triage.score_text",
            "scorer_status": "active",
            "score_schema": "schemas/scoring/minimal-triage-score-v0.schema.json",
            "calibration_profile_id": CALIBRATION_PROFILE_ID,
            "inputs": ["candidate output text"],
            "outputs": ["minimal triage score", "legacy confidence label"],
            "notes": [
                "Deterministic local triage scorer used by bounded CPU stages.",
                "Raw labels are mapped through Stage 4I compatibility records.",
            ],
            "solve_claim": False,
            "trusted_as_canonical": False,
            "cuda_used": False,
        },
        {
            "record_type": "scorer_record",
            "scorer_id": "stage3c_calibrated_minimal_triage_v0",
            "scorer_version": "stage3c-calibration-v0",
            "module": "libreprimus.scoring.calibration.classify_score",
            "scorer_status": "active",
            "score_schema": "schemas/scoring/score-summary-record-v0.schema.json",
            "calibration_profile_id": CALIBRATION_PROFILE_ID,
            "inputs": ["minimal triage score", "crib check", "Stage 3C thresholds"],
            "outputs": ["calibrated confidence label"],
            "notes": ["Calibration labels are triage metadata only."],
            "solve_claim": False,
            "trusted_as_canonical": False,
            "cuda_used": False,
        },
        {
            "record_type": "scorer_record",
            "scorer_id": "crib_check_v0",
            "scorer_version": "crib-check-result-v0",
            "module": "libreprimus.scoring.crib_checks.crib_check",
            "scorer_status": "compatibility_only",
            "score_schema": "schemas/scoring/crib-check-result-v0.schema.json",
            "calibration_profile_id": CALIBRATION_PROFILE_ID,
            "inputs": ["candidate output text", "tiny committed crib list"],
            "outputs": ["crib hits"],
            "notes": ["Crib hits are weak triage features and cannot validate plaintext alone."],
            "solve_claim": False,
            "trusted_as_canonical": False,
            "cuda_used": False,
        },
    ]
