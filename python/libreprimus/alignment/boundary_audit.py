"""Page-boundary confidence audit for Stage 0D-followup."""

from __future__ import annotations

from collections import Counter

from libreprimus.alignment.models import (
    PageBoundaryAuditSummary,
    PageBoundaryCandidate,
    PageBoundaryConfidenceAudit,
)

EXPECTED_LP2_PAGE_COUNT = 58


def _empty_pair_only(boundary: PageBoundaryCandidate) -> bool:
    evidence = " ".join(boundary.evidence).lower()
    return "empty" in evidence and not boundary.explicit_marker and not boundary.anchor_supported and boundary.aligned_pair_count_near_boundary == 0


def audit_page_boundaries(
    boundaries: list[PageBoundaryCandidate],
    *,
    expected_lp2_page_count: int = EXPECTED_LP2_PAGE_COUNT,
) -> tuple[list[PageBoundaryConfidenceAudit], PageBoundaryAuditSummary]:
    """Audit non-canonical boundary candidates against stricter confidence rules."""
    audits: list[PageBoundaryConfidenceAudit] = []
    for boundary in boundaries:
        empty_only = _empty_pair_only(boundary)
        warnings = list(boundary.warnings)
        if boundary.confidence == "high" and empty_only:
            warnings.append("Empty-pair-only evidence cannot support high boundary confidence.")
        if boundary.confidence == "high" and boundary.aligned_pair_count_near_boundary == 0 and not boundary.explicit_marker:
            warnings.append("High confidence requires explicit marker, anchor support, or strong local alignment.")
        audits.append(
            PageBoundaryConfidenceAudit(
                record_type="page_boundary_confidence_audit",
                candidate_page_label=boundary.candidate_page_label,
                candidate_local_page_index=boundary.candidate_local_page_index,
                start_pair_index=boundary.start_pair_index,
                end_pair_index=boundary.end_pair_index,
                confidence=boundary.confidence,
                previous_policy_confidence="high" if boundary.explicit_marker or boundary.anchor_supported else boundary.confidence,
                downgraded_from_previous_policy=boundary.downgraded_from_previous_policy,
                explicit_marker=boundary.explicit_marker,
                anchor_supported=boundary.anchor_supported,
                aligned_pair_count_near_boundary=boundary.aligned_pair_count_near_boundary,
                no_match_count_near_boundary=boundary.no_match_count_near_boundary,
                empty_pair_only=empty_only,
                canonical_page_boundary=boundary.canonical_page_boundary,
                evidence=boundary.evidence,
                warnings=warnings,
            )
        )

    confidence_counts = Counter(boundary.confidence for boundary in boundaries)
    parable = next(
        (
            boundary.confidence
            for boundary in boundaries
            if boundary.candidate_page_label == "57.jpg" or "Parable anchor matched" in " ".join(boundary.evidence)
        ),
        None,
    )
    exceeds = len(boundaries) > expected_lp2_page_count
    summary = PageBoundaryAuditSummary(
        record_type="page_boundary_audit",
        total_boundary_candidates=len(boundaries),
        high_count=confidence_counts["high"],
        medium_count=confidence_counts["medium"],
        low_count=confidence_counts["low"],
        none_count=confidence_counts["none"],
        overgeneration_warning=exceeds,
        candidates_exceed_expected_lp2_page_count=exceeds,
        candidates_with_explicit_marker=sum(1 for boundary in boundaries if boundary.explicit_marker),
        candidates_with_anchor=sum(1 for boundary in boundaries if boundary.anchor_supported),
        candidates_from_empty_pair_only=sum(1 for audit in audits if audit.empty_pair_only),
        candidates_downgraded_from_previous_policy=sum(1 for boundary in boundaries if boundary.downgraded_from_previous_policy),
        parable_candidate_confidence=parable,
        canonical_page_boundary_all_false=all(not boundary.canonical_page_boundary for boundary in boundaries),
        trusted_as_canonical=False,
    )
    return audits, summary
