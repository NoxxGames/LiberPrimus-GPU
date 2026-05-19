from __future__ import annotations

from libreprimus.source_delta_audit.image_artifact_backlog import build_image_artifact_observations


def test_image_artifact_observation_is_future_preflight_only() -> None:
    record = build_image_artifact_observations()[0]
    assert record["usable_as_experiment_seed"] is False
    assert record["solve_claim"] is False
    assert record["review_status"] == "future_preflight"
    assert "DCT/blockiness estimate" in record["future_tests"]
    assert record["negative_controls"]
