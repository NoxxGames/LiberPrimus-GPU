"""Review-only image artifact candidates for Stage 4M."""

from __future__ import annotations

from typing import Any

from libreprimus.image_preflight.models import COMMON_FALSE_FLAGS


def build_artifact_candidates(compression_observations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Convert committed artifact observations into review-only Stage 4M candidates."""

    records: list[dict[str, Any]] = []
    for observation in compression_observations:
        observation_id = str(observation.get("observation_id") or observation.get("record_id") or "unknown")
        records.append(
            {
                "record_type": "image_artifact_review_candidate",
                "candidate_id": f"stage4m-artifact-candidate-{observation_id}",
                "source_observation_id": observation_id,
                "artifact_type": observation.get("artifact_type", "compression_like_artifact"),
                "review_state": "future_preflight",
                "artifact_review_status": "review_only",
                "source_variant_required": True,
                "negative_controls_required": True,
                "ordinary_compression_null_controls_required": True,
                "negative_control_note": (
                    "Compression and star-like features are suitable for future false-positive controls; "
                    "they are not evidence of intentional hidden data."
                ),
                "notes": observation.get("notes") or "Stage 4M records this as review-only preflight.",
                **COMMON_FALSE_FLAGS,
            }
        )
    if not records:
        records.append(
            {
                "record_type": "image_artifact_review_candidate",
                "candidate_id": "stage4m-artifact-candidate-compression-like-placeholder",
                "source_observation_id": None,
                "artifact_type": "compression_like_artifact",
                "review_state": "future_preflight",
                "artifact_review_status": "review_only",
                "source_variant_required": True,
                "negative_controls_required": True,
                "ordinary_compression_null_controls_required": True,
                "notes": "Placeholder review-only candidate; no committed Stage 4E observation found.",
                **COMMON_FALSE_FLAGS,
            }
        )
    return records
