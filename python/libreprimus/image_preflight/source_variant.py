"""Source-variant readiness records for Stage 4M."""

from __future__ import annotations

from typing import Any

from libreprimus.image_preflight.models import COMMON_FALSE_FLAGS


def build_source_variant_records(
    metadata_records: list[dict[str, Any]],
    *,
    image_locks: list[dict[str, Any]],
    image_artifacts: list[dict[str, Any]],
    source_delta_records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Compare local image metadata against committed locks and known variant categories."""

    locks_by_relative_path = {
        str(record.get("relative_path")): record for record in image_locks if record.get("relative_path")
    }
    artifacts_by_relative_path = {
        str(record.get("relative_path")): record for record in image_artifacts if record.get("relative_path")
    }
    variant_categories = _variant_categories(source_delta_records)
    records: list[dict[str, Any]] = []
    for metadata in metadata_records:
        relative_path = str(metadata["relative_path"])
        lock = locks_by_relative_path.get(relative_path)
        artifact = artifacts_by_relative_path.get(relative_path)
        lock_sha256 = lock.get("sha256") if lock else None
        lock_matched = lock_sha256 == metadata["sha256"] if lock_sha256 else False
        status = "blocked_external_variant_not_cached"
        if not lock:
            status = "blocked_missing_local_lock"
        records.append(
            {
                "record_type": "image_source_variant_preflight_record",
                "preflight_record_id": f"stage4m-source-variant-{metadata['image_id']}",
                "image_id": metadata["image_id"],
                "relative_path": relative_path,
                "file_name": metadata["file_name"],
                "sha256": metadata["sha256"],
                "local_lock_record_present": lock is not None,
                "local_lock_sha256_matches": lock_matched,
                "artifact_record_present": artifact is not None,
                "external_variant_metadata_available": bool(variant_categories),
                "external_variant_categories": variant_categories,
                "source_variant_status": status,
                "notes": "External variant bytes were not downloaded or compared in Stage 4M.",
                **COMMON_FALSE_FLAGS,
            }
        )
    return records


def _variant_categories(source_delta_records: list[dict[str, Any]]) -> list[str]:
    categories: set[str] = set()
    for record in source_delta_records:
        for candidate in record.get("selected_path_candidates") or []:
            artifact_type = str(candidate.get("artifact_type") or "")
            if artifact_type in {"lp_full_image", "lp_unsolved_image"}:
                categories.add(artifact_type)
        category_counts = record.get("category_counts") or {}
        for artifact_type in ("lp_full_image", "lp_unsolved_image"):
            if artifact_type in category_counts:
                categories.add(artifact_type)
    return sorted(categories)
