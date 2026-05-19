"""Stage 4J observation review policy records."""

from __future__ import annotations

from libreprimus.observation_review.models import OBSERVATION_TYPES, PROMOTION_GATES, REVIEW_STATES


def build_policy_record() -> dict:
    """Return the committed Stage 4J review policy."""

    return {
        "record_type": "observation_review_policy",
        "policy_id": "stage4j-observation-review-policy-v0",
        "stage": "stage4j",
        "review_states": list(REVIEW_STATES),
        "observation_types": list(OBSERVATION_TYPES),
        "promotion_gates": list(PROMOTION_GATES),
        "review_principles": [
            "observation_records_are_not_truth_until_reviewed",
            "scoring_is_triage_not_proof",
            "visual_interpretation_requires_explicit_review_state",
            "review_only_observations_cannot_be_experiment_seeds",
            "negative_controls_remain_first_class_controls_without_truth_acceptance",
        ],
        "solve_claim": False,
        "trusted_as_canonical": False,
    }
