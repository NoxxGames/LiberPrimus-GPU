from __future__ import annotations

from libreprimus.observation_promotion.gates import evaluate_decision


def test_stage4l_visual_without_coordinates_cannot_be_ready() -> None:
    result = evaluate_decision(
        {
            "observation_type": "visual_cuneiform_candidate",
            "review_state": "needs_coordinates",
            "source_locked": True,
            "has_page_or_image_reference": True,
            "has_coordinates": False,
            "accepted_reading": False,
            "solve_claim": False,
        }
    )
    assert result["promotion_category"] == "blocked_needs_coordinates"
    assert result["usable_as_experiment_seed"] is False


def test_stage4l_cuneiform_without_accepted_reading_cannot_be_ready() -> None:
    result = evaluate_decision(
        {
            "observation_type": "visual_cuneiform_candidate",
            "review_state": "needs_human_review",
            "source_locked": True,
            "has_page_or_image_reference": True,
            "has_coordinates": True,
            "accepted_reading": False,
            "solve_claim": False,
        }
    )
    assert result["promotion_category"] == "blocked_needs_human_review"
    assert "cuneiform_reading_not_accepted" in result["blockers"]


def test_stage4l_ambiguous_dot_cannot_be_ready() -> None:
    result = evaluate_decision(
        {
            "observation_type": "visual_dot_pattern_candidate",
            "review_state": "quarantined",
            "source_locked": True,
            "has_page_or_image_reference": True,
            "has_coordinates": True,
            "ambiguous": True,
            "solve_claim": False,
        }
    )
    assert result["promotion_category"] == "quarantined_false_positive"
    assert result["usable_as_experiment_seed"] is False


def test_stage4l_negative_control_can_be_control_only() -> None:
    result = evaluate_decision(
        {
            "observation_type": "negative_control",
            "review_state": "negative_control",
            "source_locked": True,
            "solve_claim": False,
        }
    )
    assert result["promotion_category"] == "ready_as_control_only"


def test_stage4l_source_reference_can_be_source_reference_only() -> None:
    result = evaluate_decision(
        {
            "observation_type": "source_link",
            "review_state": "accepted",
            "source_locked": True,
            "solve_claim": False,
        }
    )
    assert result["promotion_category"] == "source_reference_only"


def test_stage4l_source_lock_missing_creates_blocker() -> None:
    result = evaluate_decision(
        {
            "observation_type": "numeric_claim",
            "review_state": "accepted",
            "source_locked": False,
            "solve_claim": False,
        }
    )
    assert result["promotion_category"] == "blocked_needs_source_lock"


def test_stage4l_bigram_fibonacci_claim_requires_reproducible_matrix() -> None:
    result = evaluate_decision(
        {
            "observation_type": "numeric_frequency_pattern_claim",
            "review_state": "needs_reproducible_matrix",
            "source_locked": False,
            "solve_claim": False,
        }
    )
    assert result["promotion_category"] == "blocked_needs_human_review"
    assert result["usable_as_experiment_seed"] is False
    assert result["blockers"] == [
        "needs_exact_transcript_profile_source",
        "needs_reproducible_bigram_matrix",
        "needs_declared_rune_order",
        "needs_diagonal_indexing_convention",
        "needs_null_controls",
        "needs_multiple_testing_controls",
    ]
