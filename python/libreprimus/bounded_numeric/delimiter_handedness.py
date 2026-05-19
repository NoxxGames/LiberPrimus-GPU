"""Stage 4D delimiter handedness metadata audit."""

from __future__ import annotations

from typing import Any

from libreprimus.bounded_numeric.manifest_loader import cap_for
from libreprimus.bounded_numeric.no_fudge_policy import enforce_cap


def audit_delimiter_handedness(manifest: dict[str, Any], delimiter_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Audit delimiter metadata without inferring reset or cipher meaning."""

    manifest_id = str(manifest.get("manifest_id"))
    cap = cap_for(manifest)
    records: list[dict[str, Any]] = []
    for item in delimiter_records:
        records.append(
            {
                "record_type": "delimiter_handedness_audit_record",
                "result_id": f"{manifest_id}-{item.get('task_id')}",
                "execution_manifest_id": manifest_id,
                "task_id": str(item.get("task_id")),
                "source_observation_id": str(item.get("source_observation_id") or ""),
                "page_refs": list(item.get("page_refs") or []),
                "delimiter_type": str(item.get("delimiter_type") or "unknown"),
                "orientation": str(item.get("orientation") or "unknown_pending_annotation"),
                "handedness": str(item.get("handedness") or "unknown_pending_annotation"),
                "coordinate_system": str(item.get("coordinate_system") or "unknown_pending_annotation"),
                "annotation_status": str(item.get("annotation_status") or "unknown"),
                "unresolved_coordinates": item.get("coordinate_system") == "unknown_pending_annotation",
                "reset_boundary_hypothesis": False,
                "meaning_inferred": False,
                "candidate_count": 1,
                "cap": cap,
                "raw_values": {
                    "orientation": str(item.get("orientation") or "unknown_pending_annotation"),
                    "handedness": str(item.get("handedness") or "unknown_pending_annotation"),
                },
                "derived_values": [
                    {
                        "name": "metadata_audit_only",
                        "formula": "count_observation_metadata_without_reset_inference",
                        "source": "stage4c_delimiter_annotation_tasks",
                        "value": True,
                    }
                ],
                "no_fudge_policy": True,
                "solve_claim": False,
                "cuda_used": False,
                "trusted_as_canonical": False,
                "generated_outputs_committed": False,
                "notes": "Delimiter metadata audit only; no reset-boundary or cipher meaning inferred.",
            }
        )
    enforce_cap(records, cap, manifest_id)
    return records


def delimiter_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Return aggregate delimiter audit counts."""

    orientation_counts: dict[str, int] = {}
    handedness_counts: dict[str, int] = {}
    unresolved = 0
    for record in records:
        orientation = str(record.get("orientation") or "unknown")
        handedness = str(record.get("handedness") or "unknown")
        orientation_counts[orientation] = orientation_counts.get(orientation, 0) + 1
        handedness_counts[handedness] = handedness_counts.get(handedness, 0) + 1
        if record.get("unresolved_coordinates") is True:
            unresolved += 1
    return {
        "delimiter_observations_audited": len(records),
        "delimiter_unresolved_coordinate_count": unresolved,
        "delimiter_orientation_counts": dict(sorted(orientation_counts.items())),
        "delimiter_handedness_counts": dict(sorted(handedness_counts.items())),
    }
