from __future__ import annotations

from libreprimus.image_preflight.source_variant import build_source_variant_records


def test_stage4m_source_variant_unavailable_blocks_external_cache() -> None:
    metadata = [
        {
            "image_id": "stage4m-lp-image-test",
            "relative_path": "third_party/LiberPrimusPages/test.jpg",
            "file_name": "test.jpg",
            "sha256": "a" * 64,
        }
    ]
    locks = [{"relative_path": "third_party/LiberPrimusPages/test.jpg", "sha256": "a" * 64}]
    source_delta = [{"category_counts": {"lp_full_image": 1, "lp_unsolved_image": 1}}]

    records = build_source_variant_records(
        metadata,
        image_locks=locks,
        image_artifacts=[],
        source_delta_records=source_delta,
    )

    assert records[0]["source_variant_status"] == "blocked_external_variant_not_cached"
    assert records[0]["local_lock_sha256_matches"] is True
    assert records[0]["usable_as_experiment_seed"] is False
