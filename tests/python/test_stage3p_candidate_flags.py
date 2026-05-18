from __future__ import annotations

from libreprimus.image_transforms.candidate_flags import build_candidate_flags


def test_visual_candidate_flags_remain_review_only() -> None:
    candidates = build_candidate_flags(
        image_id="synthetic",
        metrics={
            "left_right_mirror_difference": 0.5,
            "top_bottom_mirror_difference": 0.1,
            "rotation_180_difference": 0.02,
            "edge_density_ratio": 0.3,
            "threshold_64_foreground_ratio": 0.02,
            "threshold_128_foreground_ratio": 0.4,
            "bitplane_0_one_ratio": 0.48,
            "bitplane_1_one_ratio": 0.1,
            "component_overlay_64_largest_component_area_ratio": 0.3,
            "component_overlay_128_largest_component_area_ratio": 0.1,
            "component_overlay_192_largest_component_area_ratio": 0.1,
            "border_dark_ratio": 0.2,
        },
        output_references={
            "threshold_64": "experiments/results/image-transforms/stage3p/derived_images/synthetic/threshold_64.png",
            "threshold_128": "experiments/results/image-transforms/stage3p/derived_images/synthetic/threshold_128.png",
            "edge_difference": "experiments/results/image-transforms/stage3p/derived_images/synthetic/edge_difference.png",
            "bitplane_0": "experiments/results/image-transforms/stage3p/derived_images/synthetic/bitplane_0.png",
            "bitplane_1": "experiments/results/image-transforms/stage3p/derived_images/synthetic/bitplane_1.png",
            "component_overlay_64": "experiments/results/image-transforms/stage3p/derived_images/synthetic/component_overlay_64.png",
            "component_overlay_128": "experiments/results/image-transforms/stage3p/derived_images/synthetic/component_overlay_128.png",
            "component_overlay_192": "experiments/results/image-transforms/stage3p/derived_images/synthetic/component_overlay_192.png",
            "left_right_mirror_difference": "experiments/results/image-transforms/stage3p/derived_images/synthetic/left_right_mirror_difference.png",
        },
    )
    feature_types = {candidate["feature_type"] for candidate in candidates}

    assert "high_half_mirror_difference_candidate" in feature_types
    assert "high_rotational_symmetry_candidate" in feature_types
    assert "hidden_low_bitplane_candidate" in feature_types
    assert "high_noise_candidate" in feature_types
    for candidate in candidates:
        assert candidate["usable_as_experiment_seed"] is False
        assert candidate["solve_claim"] is False
        assert candidate["trusted_as_canonical"] is False
