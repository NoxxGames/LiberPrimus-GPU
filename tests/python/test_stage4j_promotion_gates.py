from __future__ import annotations

from libreprimus.observation_review.promotion_gates import promotion_blocked_reasons


def test_stage4j_visual_candidate_without_coordinates_cannot_promote() -> None:
    reasons = promotion_blocked_reasons(
        _decision("visual_cuneiform_candidate", review_state="accepted", has_page=True)
    )
    assert "visual_missing_coordinates" in reasons
    assert "cuneiform_missing_coordinates" in reasons


def test_stage4j_cuneiform_without_accepted_reading_cannot_promote() -> None:
    reasons = promotion_blocked_reasons(
        _decision("visual_cuneiform_candidate", review_state="accepted", has_page=True, has_coordinates=True)
    )
    assert "cuneiform_reading_not_accepted" in reasons


def test_stage4j_ambiguous_dot_candidate_cannot_promote() -> None:
    reasons = promotion_blocked_reasons(
        _decision(
            "visual_dot_pattern_candidate",
            review_state="accepted",
            has_page=True,
            has_coordinates=True,
            ambiguous=True,
        )
    )
    assert "dot_reading_ambiguous_or_unforced" in reasons


def test_stage4j_discord_candidate_requires_public_corroboration() -> None:
    reasons = promotion_blocked_reasons(
        _decision("discord_derived_lead", review_state="accepted", public_source_corroboration=False)
    )
    assert "discord_missing_public_source_corroboration" in reasons


def test_stage4j_scoring_label_cannot_create_solve_claim() -> None:
    reasons = promotion_blocked_reasons(
        {
            **_decision("numeric_claim", review_state="accepted"),
            "confidence_label": "positive_control_like",
            "solve_claim": True,
        }
    )
    assert "solve_claim_not_false" in reasons


def _decision(
    observation_type: str,
    *,
    review_state: str,
    has_page: bool = False,
    has_coordinates: bool = False,
    ambiguous: bool | None = None,
    public_source_corroboration: bool = True,
) -> dict:
    return {
        "review_decision_id": "decision-1",
        "observation_id": "obs-1",
        "source_family": "test",
        "observation_type": observation_type,
        "review_state": review_state,
        "promotion_requested": True,
        "source_locked": True,
        "has_page_or_image_reference": has_page,
        "has_coordinates": has_coordinates,
        "accepted_reading": False,
        "ambiguous": ambiguous,
        "public_source_corroboration": public_source_corroboration,
        "solve_claim": False,
        "trusted_as_canonical": False,
    }
