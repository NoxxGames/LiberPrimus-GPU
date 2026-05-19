"""Build Stage 4L promotion blocker records."""

from __future__ import annotations

from typing import Any


BLOCKER_KIND_MAP = {
    "coordinates_required": "needs_coordinates",
    "page_or_image_reference_required": "needs_coordinates",
    "source_lock_required": "needs_source_lock",
    "source_reference_not_locked": "needs_source_lock",
    "needs_human_review": "needs_human_review",
    "delimiter_meaning_not_reviewed": "needs_human_review",
    "explicit_promotion_not_requested": "needs_human_review",
    "cuneiform_reading_not_accepted": "needs_human_review",
    "ambiguous_reading": "ambiguous_reading",
    "dot_reading_ambiguous_or_unforced": "ambiguous_reading",
    "expected_output_hash_missing": "missing_expected_output",
    "toolchain_unavailable": "toolchain_unavailable",
    "stage4g_exact_cookie_refresh_zero_matches": "negative_result",
    "needs_exact_transcript_profile_source": "needs_source_lock",
    "needs_reproducible_bigram_matrix": "needs_reproducible_matrix",
    "needs_declared_rune_order": "needs_rune_order_declaration",
    "needs_diagonal_indexing_convention": "needs_indexing_convention",
    "needs_null_controls": "needs_null_controls",
    "needs_multiple_testing_controls": "needs_multiple_testing_controls",
    "quarantined_false_positive": "quarantined_false_positive",
    "rejected_by_review": "rejected",
    "source_variant_preflight_required": "deferred",
}


def build_blocker_records(decision: dict[str, Any], blockers: list[str]) -> list[dict[str, Any]]:
    """Build blocker records for one decision."""

    records: list[dict[str, Any]] = []
    decision_id = str(decision.get("review_decision_id") or "")
    observation_id = str(decision.get("observation_id") or "")
    for index, blocker in enumerate(blockers, start=1):
        records.append(
            {
                "record_type": "observation_promotion_blocker_record",
                "blocker_record_id": f"stage4l-blocker-{decision_id}-{index}",
                "review_decision_id": decision_id,
                "observation_id": observation_id,
                "observation_type": decision.get("observation_type"),
                "blocker_kind": BLOCKER_KIND_MAP.get(blocker, "deferred"),
                "reason": blocker,
                "execution_enabled": False,
                "solve_claim": False,
            }
        )
    return records
