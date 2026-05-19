from __future__ import annotations

from libreprimus.image_preflight.artifact_candidates import build_artifact_candidates


def test_stage4m_artifact_candidate_review_only_no_seed_or_solve_claim() -> None:
    records = build_artifact_candidates(
        [
            {
                "observation_id": "stage4e-lp-jpeg-like-artifact-preflight",
                "artifact_type": "jpeg_like_compression_or_source_variant",
                "notes": "Review candidate only.",
            }
        ]
    )

    assert records[0]["review_state"] == "future_preflight"
    assert records[0]["usable_as_experiment_seed"] is False
    assert records[0]["solve_claim"] is False
    assert records[0]["image_interpretation_claim"] is False
