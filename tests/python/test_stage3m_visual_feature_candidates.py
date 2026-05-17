from __future__ import annotations

from libreprimus.image_analysis.features import feature_candidates


def test_sparse_dot_like_and_high_symmetry_candidates_are_review_aids_only() -> None:
    features = feature_candidates(
        analysis_record={
            "image_id": "synthetic",
            "black_pixel_ratio": 0.01,
            "white_pixel_ratio": 0.9,
            "grayscale_stddev": 20.0,
            "both_dimensions_prime": False,
            "border_statistics": {},
            "width": 4,
            "height": 4,
        },
        threshold_records=[{"threshold": 128, "component_count": 5, "largest_component_area_ratio": 0.02}],
        symmetry_record={
            "horizontal_mirror_difference": 0.0,
            "vertical_mirror_difference": 0.02,
            "rotational_180_difference": 0.04,
        },
        bitplane_records=[{"bitplane": 0, "one_ratio": 0.5}],
    )

    feature_types = {feature["feature_type"] for feature in features}
    assert "sparse_dot_like_candidate" in feature_types
    assert "high_symmetry_candidate" in feature_types
    assert all(feature["usable_as_experiment_seed"] is False for feature in features)
    assert all(feature["solve_claim"] is False for feature in features)


def test_blank_and_high_noise_candidates_can_be_flagged_without_claims() -> None:
    features = feature_candidates(
        analysis_record={
            "image_id": "synthetic",
            "black_pixel_ratio": 0.0,
            "white_pixel_ratio": 1.0,
            "grayscale_stddev": 80.0,
            "both_dimensions_prime": False,
            "border_statistics": {},
            "width": 4,
            "height": 4,
        },
        threshold_records=[{"threshold": 128, "component_count": 0, "largest_component_area_ratio": 0.0}],
        symmetry_record={
            "horizontal_mirror_difference": 0.4,
            "vertical_mirror_difference": 0.5,
            "rotational_180_difference": 0.6,
        },
        bitplane_records=[{"bitplane": 0, "one_ratio": 0.5}],
    )

    feature_types = {feature["feature_type"] for feature in features}
    assert "blank_or_near_blank_candidate" in feature_types
    assert "high_noise_candidate" in feature_types
