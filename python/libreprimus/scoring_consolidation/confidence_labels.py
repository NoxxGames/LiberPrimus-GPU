"""Stable Stage 4I scoring confidence labels."""

from __future__ import annotations

from libreprimus.scoring_consolidation.models import CONFIDENCE_LABELS

LEGACY_LABEL_MAP = {
    "lead": "plausible_lead",
    "weak_lead": "weak_lead",
    "noisy": "noisy",
    "garbage": "garbage",
    "positive_control_like": "positive_control_like",
    "plausible_lead": "plausible_lead",
    "inconclusive": "inconclusive",
    "negative_control_like": "negative_control_like",
    "scoring_disabled": "scoring_not_available",
    "scoring_not_available": "scoring_not_available",
    "calibration_not_available": "calibration_not_available",
}


def confidence_label_records() -> list[dict[str, object]]:
    """Return the closed confidence-label vocabulary."""

    meanings = {
        "positive_control_like": "Scores in the same broad range as positive controls; review lead only.",
        "plausible_lead": "A candidate with enough calibrated features to inspect, not solve evidence.",
        "weak_lead": "A low-confidence lead requiring stronger controls before any follow-up.",
        "noisy": "Features are mixed or affected by known false-positive patterns.",
        "inconclusive": "Scoring does not support a clear positive or negative interpretation.",
        "garbage": "Triage features are strongly unlike positive controls.",
        "negative_control_like": "Matches a control class expected to produce false positives.",
        "scoring_not_available": "No score was produced for this record.",
        "calibration_not_available": "A raw score may exist, but calibration context is missing.",
    }
    actions = {
        "positive_control_like": "manual_review_required",
        "plausible_lead": "manual_review_required",
        "weak_lead": "defer_or_review_with_controls",
        "noisy": "treat_as_noise_unless_new_evidence",
        "inconclusive": "do_not_escalate_without_new_evidence",
        "garbage": "negative_or_drop",
        "negative_control_like": "preserve_as_control",
        "scoring_not_available": "record_missing_score",
        "calibration_not_available": "record_missing_calibration",
    }
    return [
        {
            "record_type": "confidence_label_record",
            "label": label,
            "meaning": meanings[label],
            "review_action": actions[label],
            "solve_claim_allowed": False,
            "cuda_used": False,
        }
        for label in CONFIDENCE_LABELS
    ]


def map_legacy_label(label: str | None) -> str:
    """Map legacy scorer labels into the Stage 4I closed label set."""

    normalized = (label or "inconclusive").strip()
    return LEGACY_LABEL_MAP.get(normalized, "inconclusive")
