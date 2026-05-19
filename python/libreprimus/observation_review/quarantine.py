"""Quarantine record creation for false-positive observation classes."""

from __future__ import annotations

from typing import Any

QUARANTINE_CLASSES = {
    "braille": "braille_overfitting",
    "constellation": "constellation_overfitting",
    "forced_13_31": "forced_13_31_readings",
    "13/31": "forced_13_31_readings",
    "cuneiform_reading_as_fact": "cuneiform_reading_treated_as_fact",
    "broad_outguess": "broad_outguess_brute_force",
    "spectrogram": "spectrogram_pareidolia",
    "ai_generated": "ai_generated_solves",
}


def build_quarantine_record(decision: dict[str, Any]) -> dict[str, Any] | None:
    """Return a quarantine/negative-control record if the decision represents a risk class."""

    state = str(decision.get("review_state"))
    if state not in {"quarantined", "negative_control"}:
        return None
    reason_text = " ".join(
        str(value)
        for value in (
            decision.get("false_positive_class"),
            decision.get("rationale"),
            " ".join(decision.get("promotion_blocked_reasons", [])),
        )
    ).lower()
    false_positive_class = _false_positive_class(reason_text, decision)
    why = decision.get("why_dangerous") or _why_dangerous(false_positive_class)
    return {
        "record_type": "observation_quarantine_record",
        "quarantine_record_id": f"stage4j-quarantine-{decision['source_family']}-{decision['observation_id']}",
        "review_decision_id": decision["review_decision_id"],
        "observation_id": decision["observation_id"],
        "observation_type": decision["observation_type"],
        "review_state": state,
        "false_positive_class": false_positive_class,
        "why_dangerous": why,
        "allowed_control_use": True,
        "truth_acceptance": False,
        "solve_claim": False,
        "trusted_as_canonical": False,
        "usable_as_experiment_seed": False,
    }


def _false_positive_class(reason_text: str, decision: dict[str, Any]) -> str:
    for marker, value in QUARANTINE_CLASSES.items():
        if marker in reason_text:
            return value
    if decision.get("observation_type") == "visual_dot_pattern_candidate":
        return "dot_pattern_ambiguity"
    if decision.get("observation_type") == "negative_control":
        return str(decision.get("false_positive_class") or "negative_control")
    return "review_quarantine"


def _why_dangerous(false_positive_class: str) -> str:
    if false_positive_class == "forced_13_31_readings":
        return "13/31 readings depend on anchor, rotation, grouping, and polarity choices."
    if false_positive_class == "cuneiform_reading_treated_as_fact":
        return "Cuneiform arithmetic can be clean while the underlying glyph segmentation is unverified."
    if false_positive_class == "spectrogram_pareidolia":
        return "Spectrogram shapes are easy to over-read without source-locked positives and controls."
    if false_positive_class == "ai_generated_solves":
        return "Generated plaintext can hallucinate and cannot replace reproducible evidence."
    return "The observation class is useful as a control but unsafe as truth evidence."
