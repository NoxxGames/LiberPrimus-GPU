"""Source health records for Stage 4F fixture candidates."""

from __future__ import annotations

from typing import Any


def build_source_health_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build source-health records for stego/audio fixture candidates."""

    health: list[dict[str, Any]] = []
    for record in records:
        artifact_type = str(record.get("artifact_type", "unknown"))
        fragility = "high" if "audio" in artifact_type or "outguessed" in artifact_type else "medium"
        health.append(
            {
                "record_type": "fixture_source_health_record",
                "source_id": str(record.get("fixture_id")),
                "source_url": str(record.get("source_url")),
                "source_path": str(record.get("source_path")),
                "fixture_kind": artifact_type,
                "health_status": "metadata_recorded_no_asset",
                "fragility": fragility,
                "retrieval_status": "source_metadata_only_stage4f",
                "recommended_action": "source-lock asset in explicit future stage",
                "raw_file_committed": False,
                "binary_committed": False,
                "audio_committed": False,
                "image_committed": False,
                "extracted_payload_committed": False,
                "font_committed": False,
                "trusted_as_canonical": False,
                "solve_claim": False,
                "notes": "Stage 4F records fixture source-health metadata only; no raw artefact is committed.",
            }
        )
    return health
