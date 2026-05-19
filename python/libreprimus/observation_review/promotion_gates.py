"""Promotion-gate checks for observation review decisions."""

from __future__ import annotations

from typing import Any

VISUAL_TYPES = {
    "visual_cuneiform_candidate",
    "visual_dot_pattern_candidate",
    "delimiter_candidate",
    "image_compression_artifact_candidate",
}


def evaluate_promotion(decision: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic promotion record for a review decision."""

    blocked_reasons = promotion_blocked_reasons(decision)
    promotion_status = "blocked" if blocked_reasons else "eligible"
    return {
        "record_type": "observation_promotion_record",
        "promotion_record_id": f"stage4j-promotion-{decision['source_family']}-{decision['observation_id']}",
        "review_decision_id": decision["review_decision_id"],
        "observation_id": decision["observation_id"],
        "observation_type": decision["observation_type"],
        "review_state": decision["review_state"],
        "promotion_status": promotion_status,
        "source_locked": bool(decision.get("source_locked")),
        "requires_coordinates": decision["observation_type"] in VISUAL_TYPES,
        "has_coordinates": bool(decision.get("has_coordinates")),
        "blocked_reasons": blocked_reasons,
        "solve_claim": False,
        "trusted_as_canonical": False,
        "usable_as_experiment_seed": False,
    }


def promotion_blocked_reasons(decision: dict[str, Any]) -> list[str]:
    """Return all policy reasons blocking candidate-manifest promotion."""

    reasons: list[str] = []
    review_state = str(decision.get("review_state"))
    observation_type = str(decision.get("observation_type"))
    if review_state not in {"accepted", "promoted_to_manifest"}:
        reasons.append("review_state_not_accepted")
    if decision.get("promotion_requested") is not True:
        reasons.append("explicit_promotion_not_requested")
    if not decision.get("source_locked") and not decision.get("synthetic_fixture"):
        reasons.append("source_not_locked")
    if decision.get("solve_claim") is not False:
        reasons.append("solve_claim_not_false")
    if decision.get("trusted_as_canonical") is not False:
        reasons.append("trusted_as_canonical_not_false")
    if observation_type in VISUAL_TYPES and not decision.get("has_page_or_image_reference"):
        reasons.append("visual_missing_page_or_image_reference")
    if observation_type in VISUAL_TYPES and not decision.get("has_coordinates") and not decision.get("non_coordinate_rationale"):
        reasons.append("visual_missing_coordinates")
    if observation_type == "visual_cuneiform_candidate":
        if not decision.get("accepted_reading"):
            reasons.append("cuneiform_reading_not_accepted")
        if not decision.get("has_coordinates"):
            reasons.append("cuneiform_missing_coordinates")
    if observation_type == "visual_dot_pattern_candidate" and decision.get("ambiguous") is not False:
        reasons.append("dot_reading_ambiguous_or_unforced")
    if observation_type == "discord_derived_lead" and decision.get("public_source_corroboration") is not True:
        reasons.append("discord_missing_public_source_corroboration")
    if review_state == "negative_control" or observation_type == "negative_control":
        reasons.append("negative_control_not_truth_candidate")
    if review_state in {"rejected", "quarantined", "deferred", "superseded"}:
        reasons.append(f"review_state_{review_state}")
    return sorted(set(reasons))
