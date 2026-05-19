from __future__ import annotations

from libreprimus.observation_review.models import REVIEW_STATES
from libreprimus.observation_review.state_machine import is_valid_review_state, transition_allowed


def test_stage4j_review_states_are_finite_and_expected() -> None:
    assert "pending" in REVIEW_STATES
    assert "promoted_to_manifest" in REVIEW_STATES
    assert is_valid_review_state("accepted")
    assert not is_valid_review_state("plaintext_verified")


def test_stage4j_review_transitions_block_invalid_jump() -> None:
    assert transition_allowed("pending", "needs_human_review")
    assert not transition_allowed("pending", "promoted_to_manifest")
    assert transition_allowed("accepted", "promoted_to_manifest")
