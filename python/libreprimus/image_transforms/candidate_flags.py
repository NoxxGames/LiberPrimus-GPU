"""Review-only visual candidate flags for Stage 3P transforms."""

from __future__ import annotations

from typing import Any

from libreprimus.image_transforms.models import REVIEW_STATUS


def build_candidate_flags(
    *,
    image_id: str,
    metrics: dict[str, float],
    output_references: dict[str, str],
) -> list[dict[str, Any]]:
    """Return deterministic visual review flags. These are not experiment seeds."""
    flags: list[tuple[str, float, dict[str, float], list[str]]] = []
    left_right = metrics.get("left_right_mirror_difference", 0.0)
    top_bottom = metrics.get("top_bottom_mirror_difference", 0.0)
    rotation = metrics.get("rotation_180_difference", 1.0)
    edge_density = metrics.get("edge_density_ratio", 0.0)
    largest_component = max(
        metrics.get("component_overlay_64_largest_component_area_ratio", 0.0),
        metrics.get("component_overlay_128_largest_component_area_ratio", 0.0),
        metrics.get("component_overlay_192_largest_component_area_ratio", 0.0),
    )
    low_bitplane = max(metrics.get("bitplane_0_one_ratio", 0.0), metrics.get("bitplane_1_one_ratio", 0.0))
    bitplane_balance = min(
        abs(metrics.get("bitplane_0_one_ratio", 0.0) - 0.5),
        abs(metrics.get("bitplane_1_one_ratio", 0.0) - 0.5),
    )

    if max(left_right, top_bottom) >= 0.28:
        flags.append(
            (
                "high_half_mirror_difference_candidate",
                max(left_right, top_bottom),
                {"left_right": left_right, "top_bottom": top_bottom},
                ["left_right_mirror_difference", "top_bottom_mirror_difference"],
            )
        )
    if rotation <= 0.08:
        flags.append(
            (
                "high_rotational_symmetry_candidate",
                1.0 - rotation,
                {"rotation_180_difference": rotation},
                ["rotation_180_difference"],
            )
        )
    if 0.005 <= metrics.get("threshold_64_foreground_ratio", 0.0) <= 0.04:
        flags.append(
            (
                "sparse_dot_like_candidate",
                1.0 - metrics.get("threshold_64_foreground_ratio", 0.0),
                {"threshold_64_foreground_ratio": metrics.get("threshold_64_foreground_ratio", 0.0)},
                ["threshold_64", "component_overlay_64"],
            )
        )
    if 0.15 <= low_bitplane <= 0.85 and bitplane_balance <= 0.25:
        flags.append(
            (
                "hidden_low_bitplane_candidate",
                1.0 - bitplane_balance,
                {
                    "bitplane_0_one_ratio": metrics.get("bitplane_0_one_ratio", 0.0),
                    "bitplane_1_one_ratio": metrics.get("bitplane_1_one_ratio", 0.0),
                },
                ["bitplane_0", "bitplane_1"],
            )
        )
    if largest_component >= 0.25:
        flags.append(
            (
                "large_component_candidate",
                largest_component,
                {"largest_component_area_ratio": largest_component},
                ["component_overlay_64", "component_overlay_128", "component_overlay_192"],
            )
        )
    if edge_density >= 0.18:
        flags.append(
            (
                "high_edge_density_candidate",
                edge_density,
                {"edge_density_ratio": edge_density},
                ["edge_difference"],
            )
        )
    if 0.04 <= metrics.get("threshold_128_foreground_ratio", 0.0) <= 0.42 and edge_density >= 0.06:
        flags.append(
            (
                "dense_rune_text_candidate",
                edge_density + metrics.get("threshold_128_foreground_ratio", 0.0),
                {
                    "edge_density_ratio": edge_density,
                    "threshold_128_foreground_ratio": metrics.get("threshold_128_foreground_ratio", 0.0),
                },
                ["edge_difference", "threshold_128"],
            )
        )
    if edge_density >= 0.25 and 0.20 <= metrics.get("threshold_128_foreground_ratio", 0.0) <= 0.80:
        flags.append(
            (
                "high_noise_candidate",
                edge_density,
                {
                    "edge_density_ratio": edge_density,
                    "threshold_128_foreground_ratio": metrics.get("threshold_128_foreground_ratio", 0.0),
                },
                ["edge_difference", "threshold_128"],
            )
        )
    if metrics.get("border_dark_ratio", 0.0) >= 0.12:
        flags.append(
            (
                "border_marker_candidate",
                metrics.get("border_dark_ratio", 0.0),
                {"border_dark_ratio": metrics.get("border_dark_ratio", 0.0)},
                ["threshold_64", "threshold_128"],
            )
        )
    if edge_density >= 0.08 and largest_component <= 0.18:
        flags.append(
            (
                "potential_symbol_cluster_candidate",
                edge_density + (0.18 - largest_component),
                {"edge_density_ratio": edge_density, "largest_component_area_ratio": largest_component},
                ["edge_difference", "component_overlay_128"],
            )
        )

    return [
        {
            "record_type": "visual_transform_candidate",
            "candidate_id": f"{image_id}-{feature_type}",
            "image_id": image_id,
            "feature_type": feature_type,
            "transform_names": transform_names,
            "feature_score": round(float(score), 8),
            "evidence_fields": evidence,
            "review_status": REVIEW_STATUS,
            "output_references": [
                output_references[name] for name in transform_names if name in output_references
            ],
            "trusted_as_canonical": False,
            "usable_as_experiment_seed": False,
            "solve_claim": False,
            "notes": "Deterministic Stage 3P visual review flag only; not interpreted as meaning.",
        }
        for feature_type, score, evidence, transform_names in flags
    ]
