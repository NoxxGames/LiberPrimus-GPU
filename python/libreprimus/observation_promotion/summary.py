"""Summaries for Stage 4L observation promotion."""

from __future__ import annotations

from collections import Counter
from typing import Any


def summarize_promotion(
    *,
    decisions: list[dict[str, Any]],
    ledger_records: list[dict[str, Any]],
    readiness_records: list[dict[str, Any]],
    blocker_records: list[dict[str, Any]],
    manifest_readiness_records: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build a committed Stage 4L summary."""

    categories = Counter(str(record.get("promotion_category") or "") for record in readiness_records)
    observation_types = Counter(str(record.get("observation_type") or "") for record in readiness_records)
    cuneiform = _type_counts(readiness_records, "visual_cuneiform_candidate")
    dots = _type_counts(readiness_records, "visual_dot_pattern_candidate")
    cookies = _type_counts(readiness_records, "cookie_hash_candidate")
    stego_audio = _type_counts(readiness_records, "stego_audio_fixture_candidate")
    manifest_states = Counter(str(record.get("ready_state") or "") for record in manifest_readiness_records)
    blocked_count = sum(count for category, count in categories.items() if category.startswith("blocked_"))
    return {
        "record_type": "reviewed_observation_promotion_summary",
        "stage": "stage4l",
        "reviewed_observations_loaded": len(decisions),
        "ledger_records_created": len(ledger_records),
        "readiness_records_created": len(readiness_records),
        "blocker_records_created": len(blocker_records),
        "manifest_readiness_records_created": len(manifest_readiness_records),
        "ready_for_manifest_count": categories["ready_for_manifest"],
        "ready_as_control_only_count": categories["ready_as_control_only"],
        "source_reference_only_count": categories["source_reference_only"],
        "blocked_count": blocked_count,
        "deferred_count": categories["deferred"],
        "quarantined_count": categories["quarantined_false_positive"],
        "rejected_count": categories["rejected"],
        "cuneiform_ready_count": cuneiform["ready_for_manifest"],
        "cuneiform_deferred_count": cuneiform["deferred"],
        "cuneiform_blocker_count": cuneiform["blocked"],
        "dot_ready_count": dots["ready_for_manifest"],
        "dot_quarantined_count": dots["quarantined_false_positive"],
        "dot_blocker_count": dots["blocked"],
        "cookie_ready_count": cookies["ready_for_manifest"],
        "cookie_blocked_count": cookies["blocked"],
        "stego_audio_ready_count": stego_audio["ready_for_manifest"],
        "stego_audio_deferred_count": stego_audio["deferred"],
        "stego_audio_blocker_count": stego_audio["blocked"],
        "manifest_ready_count": manifest_states["ready"],
        "manifest_control_only_count": manifest_states["control_only"],
        "manifest_blocked_count": manifest_states["blocked"],
        "manifest_deferred_count": manifest_states["deferred"],
        "category_counts": dict(sorted(categories.items())),
        "observation_type_counts": dict(sorted(observation_types.items())),
        "manifest_ready_state_counts": dict(sorted(manifest_states.items())),
        "execution_enabled": False,
        "solve_claim": False,
        "trusted_as_canonical": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "cuda_used": False,
        "generated_outputs_committed": False,
        "raw_data_processed": False,
    }


def load_summary(path) -> dict[str, Any]:
    """Load a Stage 4L summary document."""

    from libreprimus.observation_promotion.loaders import load_yaml_records

    records = load_yaml_records(path)
    return records[0] if records else {}


def _type_counts(records: list[dict[str, Any]], observation_type: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    for record in records:
        if record.get("observation_type") != observation_type:
            continue
        category = str(record.get("promotion_category") or "")
        if category == "ready_for_manifest":
            counts["ready_for_manifest"] += 1
        elif category == "deferred":
            counts["deferred"] += 1
        elif category == "quarantined_false_positive":
            counts["quarantined_false_positive"] += 1
            counts["blocked"] += 1
        elif category.startswith("blocked_") or category in {"rejected"}:
            counts["blocked"] += 1
    return counts
