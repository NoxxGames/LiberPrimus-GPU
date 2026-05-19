"""Summary helpers for Stage 4J observation review."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

import yaml


def summarize_review(
    *,
    decisions: list[dict[str, Any]],
    promotions: list[dict[str, Any]],
    quarantines: list[dict[str, Any]],
    path_summary: dict[str, Any],
) -> dict[str, Any]:
    """Build the committed Stage 4J summary record."""

    state_counts = Counter(str(record.get("review_state")) for record in decisions)
    return {
        "record_type": "observation_review_summary",
        "stage": "stage4j",
        "observations_loaded": len(decisions),
        "decisions_created": len(decisions),
        "accepted_count": state_counts["accepted"],
        "rejected_count": state_counts["rejected"],
        "deferred_count": state_counts["deferred"],
        "quarantined_count": state_counts["quarantined"],
        "negative_control_count": state_counts["negative_control"],
        "promoted_to_manifest_count": state_counts["promoted_to_manifest"],
        "promotion_record_count": len(promotions),
        "quarantine_record_count": len(quarantines),
        "visual_observations_blocked_from_seed_count": sum(
            1
            for record in decisions
            if str(record.get("observation_type")).startswith("visual")
            and record.get("usable_as_experiment_seed") is False
        ),
        "cuneiform_blocked_or_deferred_count": sum(
            1 for record in decisions if record.get("observation_type") == "visual_cuneiform_candidate"
        ),
        "dot_ambiguity_blocked_or_quarantined_count": sum(
            1 for record in decisions if record.get("observation_type") == "visual_dot_pattern_candidate"
        ),
        "path_sanitisation_passed": bool(path_summary.get("path_sanitisation_passed")),
        "path_sanitisation_findings_count": int(path_summary.get("absolute_local_path_finding_count", 0)),
        "stale_operational_text_finding_count": int(path_summary.get("stale_operational_text_finding_count", 0)),
        "solve_claim": False,
        "trusted_as_canonical": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "generated_outputs_committed": False,
    }


def load_summary(path: Path) -> dict[str, Any]:
    """Load the committed Stage 4J summary."""

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Summary must be a YAML object: {path}")
    return data
