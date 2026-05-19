"""Observation review state helpers."""

from __future__ import annotations

from libreprimus.observation_review.models import REVIEW_STATES

ALLOWED_TRANSITIONS = {
    "pending": {"needs_human_review", "needs_source_lock", "needs_coordinates", "deferred", "quarantined"},
    "needs_human_review": {"accepted", "rejected", "deferred", "quarantined", "needs_coordinates", "negative_control"},
    "needs_source_lock": {"needs_human_review", "accepted", "rejected", "deferred", "quarantined"},
    "needs_coordinates": {"needs_human_review", "accepted", "deferred", "quarantined", "negative_control"},
    "accepted": {"promoted_to_manifest", "superseded"},
    "rejected": {"negative_control", "superseded"},
    "deferred": {"needs_human_review", "needs_source_lock", "needs_coordinates", "superseded"},
    "quarantined": {"negative_control", "superseded"},
    "superseded": set(),
    "negative_control": {"superseded"},
    "promoted_to_manifest": {"superseded"},
}


def is_valid_review_state(state: str) -> bool:
    """Return true when `state` is a Stage 4J review state."""

    return state in REVIEW_STATES


def transition_allowed(from_state: str, to_state: str) -> bool:
    """Return true when the lifecycle permits the transition."""

    return to_state in ALLOWED_TRANSITIONS.get(from_state, set())
