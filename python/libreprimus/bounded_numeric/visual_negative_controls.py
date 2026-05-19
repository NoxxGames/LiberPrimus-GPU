"""Stage 4D visual negative-control ambiguity audits."""

from __future__ import annotations

from typing import Any

from libreprimus.bounded_numeric.manifest_loader import cap_for
from libreprimus.bounded_numeric.no_fudge_policy import enforce_cap


def audit_dot_ambiguity(manifest: dict[str, Any], dot_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Audit dot-pattern ambiguity without promoting readings."""

    manifest_id = str(manifest.get("manifest_id"))
    cap = cap_for(manifest)
    records: list[dict[str, Any]] = []
    for item in dot_records:
        possible = [str(value) for value in item.get("possible_readings", []) or []]
        claimed = [str(value) for value in item.get("claimed_readings", []) or []]
        records.append(
            {
                "record_type": "bounded_numeric_result_record",
                "result_id": f"{manifest_id}-{item.get('task_id')}",
                "execution_manifest_id": manifest_id,
                "audit_type": "dot_ambiguity_audit",
                "status": "audited_ambiguity_only",
                "candidate_count": 1,
                "cap": cap,
                "raw_values": {
                    "possible_readings": possible,
                    "claimed_readings": claimed,
                    "ordering_policy": item.get("ordering_policy"),
                    "polarity_policy": item.get("polarity_policy"),
                },
                "derived_values": [
                    {
                        "name": "possible_reading_count",
                        "formula": "count(possible_readings)",
                        "source": "stage4c_dot_pattern_annotation_tasks",
                        "value": len(possible),
                    },
                    {
                        "name": "claimed_reading_uniqueness",
                        "formula": "len(possible_readings) == 1 and claimed_readings subset possible_readings",
                        "source": "stage4c_dot_pattern_annotation_tasks",
                        "value": len(set(possible)) == 1 and set(claimed) <= set(possible),
                    },
                ],
                "claimed_reading_uniqueness": len(set(possible)) == 1 and set(claimed) <= set(possible),
                "polarity_orientation_dependent": True,
                "no_fudge_policy": True,
                "solve_claim": False,
                "cuda_used": False,
                "trusted_as_canonical": False,
                "generated_outputs_committed": False,
                "notes": "Dot 13/31 readings remain ambiguous and unforced.",
            }
        )
    enforce_cap(records, cap, manifest_id)
    return records


def audit_visual_negative_controls(
    manifest: dict[str, Any],
    negative_records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Create numeric ambiguity records for visual false-positive classes."""

    manifest_id = str(manifest.get("manifest_id"))
    cap = cap_for(manifest)
    records: list[dict[str, Any]] = []
    for item in negative_records:
        false_positive_class = str(item.get("false_positive_class") or "")
        records.append(
            {
                "record_type": "numeric_negative_control_result",
                "result_id": f"{manifest_id}-{item.get('task_id')}",
                "execution_manifest_id": manifest_id,
                "negative_control_id": str(item.get("task_id") or item.get("source_negative_control_id") or ""),
                "source_negative_control_id": str(item.get("source_negative_control_id") or ""),
                "false_positive_class": false_positive_class,
                "possible_reading_count": _default_possible_count(false_positive_class),
                "claimed_reading_uniqueness": False,
                "polarity_orientation_dependent": _depends_on_orientation(false_positive_class),
                "ambiguity_metric": _ambiguity_metric(false_positive_class),
                "why_dangerous": str(item.get("why_dangerous") or ""),
                "required_null_control": str(item.get("required_null_control") or ""),
                "no_fudge_policy": True,
                "solve_claim": False,
                "cuda_used": False,
                "trusted_as_canonical": False,
                "generated_outputs_committed": False,
                "notes": "Negative-control audit only; not a cipher candidate.",
            }
        )
    enforce_cap(records, cap, manifest_id)
    return records


def _default_possible_count(false_positive_class: str) -> int:
    if "forced_13_31" in false_positive_class:
        return 11
    if "braille" in false_positive_class or "constellation" in false_positive_class:
        return 64
    if "cuneiform" in false_positive_class or "base60" in false_positive_class:
        return 2
    return 0


def _depends_on_orientation(false_positive_class: str) -> bool:
    return any(term in false_positive_class for term in ("dot", "braille", "constellation", "geometry", "mayfly"))


def _ambiguity_metric(false_positive_class: str) -> str:
    if _depends_on_orientation(false_positive_class):
        return "orientation_or_polarity_dependent"
    if "cuneiform" in false_positive_class or "base60" in false_positive_class:
        return "reading_depends_on_visual_segmentation"
    return "not_numeric_claim_or_source_missing"
