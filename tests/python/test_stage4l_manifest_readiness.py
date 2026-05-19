from __future__ import annotations

from libreprimus.observation_promotion.manifest_readiness import build_manifest_readiness_records


def test_stage4l_manifest_readiness_never_enables_execution() -> None:
    records = build_manifest_readiness_records()
    assert len(records) == 13
    assert all(record["execution_enabled"] is False for record in records)
    assert all(record["solve_claim"] is False for record in records)
    assert all(record["no_solve_claim"] is True for record in records)
    assert all(record["cuda_enabled"] is False for record in records)
    assert {record["future_manifest_id"] for record in records} >= {
        "cookie_pack_v2",
        "visual_negative_controls_v1",
        "image_compression_artifact_preflight",
        "exp_stage4m_bigram_diagonal_fibonacci_421_audit",
    }


def test_stage4l_bigram_manifest_readiness_is_blocked() -> None:
    records = {
        record["future_manifest_id"]: record
        for record in build_manifest_readiness_records()
    }
    record = records["exp_stage4m_bigram_diagonal_fibonacci_421_audit"]
    assert record["ready_state"] == "blocked"
    assert record["blockers"] == [
        "needs_reproducible_bigram_matrix",
        "needs_declared_rune_order",
        "needs_null_model",
        "needs_pattern_predefinition",
    ]
