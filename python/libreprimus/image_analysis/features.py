"""Review-only visual feature candidate flags."""

from __future__ import annotations

from typing import Any


def feature_candidates(
    *,
    analysis_record: dict[str, Any],
    threshold_records: list[dict[str, Any]],
    symmetry_record: dict[str, Any],
    bitplane_records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Emit deterministic review-aid feature candidates without interpretation."""
    image_id = str(analysis_record["image_id"])
    records: list[dict[str, Any]] = []
    black_ratio = float(analysis_record["black_pixel_ratio"])
    white_ratio = float(analysis_record["white_pixel_ratio"])
    stddev = float(analysis_record["grayscale_stddev"])
    both_prime = bool(analysis_record.get("both_dimensions_prime", False))
    largest_128 = _threshold(threshold_records, 128)
    component_count_128 = int(largest_128.get("component_count", 0)) if largest_128 else 0
    largest_area_128 = float(largest_128.get("largest_component_area_ratio", 0.0)) if largest_128 else 0.0
    min_symmetry = min(
        float(symmetry_record["horizontal_mirror_difference"]),
        float(symmetry_record["vertical_mirror_difference"]),
        float(symmetry_record["rotational_180_difference"]),
    )
    max_symmetry = max(
        float(symmetry_record["horizontal_mirror_difference"]),
        float(symmetry_record["vertical_mirror_difference"]),
        float(symmetry_record["rotational_180_difference"]),
    )
    border_stats = dict(analysis_record.get("border_statistics", {}))
    border_dark = max(
        float(border_stats.get("top_dark_ratio", 0.0)),
        float(border_stats.get("bottom_dark_ratio", 0.0)),
        float(border_stats.get("left_dark_ratio", 0.0)),
        float(border_stats.get("right_dark_ratio", 0.0)),
    )
    bitplane_extreme = max(
        abs(float(record["one_ratio"]) - 0.5) for record in bitplane_records
    ) if bitplane_records else 0.0

    if min_symmetry <= 0.05:
        records.append(_record(image_id, "high_symmetry_candidate", 1.0 - min_symmetry, {"min_symmetry": min_symmetry}))
    if min_symmetry >= 0.35:
        records.append(_record(image_id, "high_asymmetry_candidate", min_symmetry, {"min_symmetry": min_symmetry}))
    if 0.0005 <= black_ratio <= 0.05 and 1 <= component_count_128 <= 400:
        records.append(
            _record(
                image_id,
                "sparse_dot_like_candidate",
                max(0.0, 0.05 - black_ratio),
                {"black_pixel_ratio": black_ratio, "component_count_128": component_count_128},
            )
        )
    if 0.03 <= black_ratio <= 0.45 and component_count_128 >= 50:
        records.append(
            _record(
                image_id,
                "dense_text_like_candidate",
                min(1.0, black_ratio + component_count_128 / 1000),
                {"black_pixel_ratio": black_ratio, "component_count_128": component_count_128},
            )
        )
    if largest_area_128 >= 0.1:
        records.append(
            _record(
                image_id,
                "large_black_component_candidate",
                largest_area_128,
                {"largest_component_area_ratio_128": largest_area_128},
            )
        )
    if border_dark >= 0.2:
        records.append(_record(image_id, "border_marker_candidate", border_dark, {"max_border_dark_ratio": border_dark}))
    if bitplane_extreme >= 0.45:
        records.append(
            _record(image_id, "low_bitplane_anomaly_candidate", bitplane_extreme, {"bitplane_extreme": bitplane_extreme})
        )
    if both_prime:
        records.append(
            _record(
                image_id,
                "prime_dimension_candidate",
                1.0,
                {"width": analysis_record["width"], "height": analysis_record["height"]},
            )
        )
    if black_ratio <= 0.001 and white_ratio >= 0.98:
        records.append(
            _record(
                image_id,
                "blank_or_near_blank_candidate",
                white_ratio,
                {"black_pixel_ratio": black_ratio, "white_pixel_ratio": white_ratio},
            )
        )
    if stddev >= 70 and max_symmetry >= 0.25:
        records.append(
            _record(
                image_id,
                "high_noise_candidate",
                min(1.0, stddev / 128),
                {"grayscale_stddev": stddev, "max_symmetry_difference": max_symmetry},
            )
        )
    return records


def _threshold(records: list[dict[str, Any]], threshold: int) -> dict[str, Any] | None:
    for record in records:
        if record.get("threshold") == threshold:
            return record
    return None


def _record(image_id: str, feature_type: str, score: float, evidence_fields: dict[str, Any]) -> dict[str, Any]:
    return {
        "record_type": "visual_feature_candidate",
        "image_id": image_id,
        "feature_id": f"{image_id}-{feature_type}",
        "feature_type": feature_type,
        "feature_score": round(score, 8),
        "evidence_fields": evidence_fields,
        "review_status": "human_review_required",
        "usable_as_experiment_seed": False,
        "trusted_as_canonical": False,
        "solve_claim": False,
        "notes": "Deterministic Stage 3M review aid only; not an experiment seed.",
    }
