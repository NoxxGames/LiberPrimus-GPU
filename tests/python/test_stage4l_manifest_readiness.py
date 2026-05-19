from __future__ import annotations

from libreprimus.observation_promotion.manifest_readiness import build_manifest_readiness_records


def test_stage4l_manifest_readiness_never_enables_execution() -> None:
    records = build_manifest_readiness_records()
    assert len(records) == 12
    assert all(record["execution_enabled"] is False for record in records)
    assert all(record["solve_claim"] is False for record in records)
    assert {record["future_manifest_id"] for record in records} >= {
        "cookie_pack_v2",
        "visual_negative_controls_v1",
        "image_compression_artifact_preflight",
    }
