"""Models for bounded candidate inspection summaries."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class InspectionSummary:
    results_dir: str
    run_id: str
    candidate_count: int
    top_n: int
    top_candidate: dict[str, Any]
    refined_top_candidate: dict[str, Any] | None
    transform_family_counts: dict[str, int]
    top_transform_family_counts: dict[str, int]
    score_distribution: dict[str, float]
    score_gaps: dict[str, float]
    diagnostics: dict[str, Any]
    qualitative_label: str
    recommendation: str
    warnings: list[str] = field(default_factory=list)
