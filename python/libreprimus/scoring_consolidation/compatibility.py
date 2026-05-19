"""Compatibility mapping for historical scoring labels and fields."""

from __future__ import annotations

from libreprimus.scoring_consolidation.confidence_labels import LEGACY_LABEL_MAP


def compatibility_records() -> list[dict[str, object]]:
    """Return committed mapping records from legacy labels to Stage 4I labels."""

    records: list[dict[str, object]] = []
    for source, target in sorted(LEGACY_LABEL_MAP.items()):
        records.append(
            {
                "record_type": "scorer_compatibility_map",
                "source_label": source,
                "target_label": target,
                "source_context": _source_context(source),
                "mapping_kind": _mapping_kind(source),
                "solve_claim": False,
                "trusted_as_canonical": False,
                "cuda_used": False,
            }
        )
    return records


def _mapping_kind(source: str) -> str:
    if source in {"lead", "weak_lead", "noisy", "garbage"}:
        return "legacy_minimal_triage"
    if source in {"scoring_disabled", "scoring_not_available", "calibration_not_available"}:
        return "availability_status"
    return "identity"


def _source_context(source: str) -> str:
    if source in {"lead", "weak_lead", "noisy", "garbage"}:
        return "libreprimus.scoring.minimal_triage confidence_label"
    if source in {"scoring_disabled", "scoring_not_available", "calibration_not_available"}:
        return "CPU batch scoring availability status"
    return "Stage 3C calibrated confidence label"
