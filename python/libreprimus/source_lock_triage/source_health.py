"""Source-health record construction for Stage 4B."""

from __future__ import annotations

from typing import Any


def build_source_health_records(source_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Create metadata-only health records for promoted sources."""

    records: list[dict[str, Any]] = []
    for source in source_records:
        source_class = str(source.get("source_class", ""))
        classification = str(source.get("classification", ""))
        if classification in {"unsafe_or_private", "ignore_for_now"}:
            continue
        fragility = "medium"
        health_status = "not_fetched_stage4b"
        if source_class == "strong_community_technical":
            fragility = "medium"
        elif source_class == "secondary_archive":
            fragility = "high"
        elif source_class == "reference_only_tooling":
            fragility = "medium"
            health_status = "reference_only"
        elif source_class == "speculative":
            fragility = "high"
        records.append(
            {
                "record_type": "source_health_record",
                "source_id": source["source_id"],
                "url": source["url"],
                "source_class": source_class,
                "health_status": health_status,
                "fragility": fragility,
                "checked_at_stage": "stage4b",
                "retrieval_status": "metadata_recorded_not_fetched_stage4b",
                "recommended_action": source.get("recommended_action", "source-lock now"),
                "trusted_as_canonical": False,
                "solve_claim": False,
                "notes": "Stage 4B records source-health metadata only; no broad fetch or mirror occurred.",
            }
        )
    return records
