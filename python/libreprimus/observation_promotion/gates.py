"""Promotion gate evaluation for Stage 4L."""

from __future__ import annotations

from typing import Any

from libreprimus.observation_promotion.models import LOCKED_SOURCE_STATUSES


def source_lock_for_decision(
    decision: dict[str, Any],
    source_lock_by_candidate: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    """Find the best Stage 4K source-lock record for a Stage 4J decision."""

    candidates = [
        str(decision.get("observation_id") or ""),
        str(decision.get("source_payload", {}).get("source_id") if isinstance(decision.get("source_payload"), dict) else ""),
    ]
    review_id = str(decision.get("review_decision_id") or "")
    for candidate_id, record in source_lock_by_candidate.items():
        if candidate_id in candidates or candidate_id in review_id:
            return record
    return None


def evaluate_decision(
    decision: dict[str, Any],
    source_lock: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Evaluate one reviewed observation against Stage 4L promotion gates."""

    observation_type = str(decision.get("observation_type") or "")
    review_state = str(decision.get("review_state") or "")
    source_status = _source_lock_status(decision, source_lock)
    blockers: list[str] = []

    if decision.get("solve_claim") is not False:
        blockers.append("solve_claim_not_allowed")
    if review_state == "rejected":
        return _result("rejected", ["rejected_by_review"], source_status)
    if review_state == "quarantined":
        return _result("quarantined_false_positive", ["quarantined_false_positive"], source_status)
    if review_state == "negative_control" or observation_type == "negative_control":
        return _result("ready_as_control_only", [], source_status)
    if observation_type == "source_link":
        if review_state == "accepted" and _is_locked(source_status):
            return _result("source_reference_only", [], source_status)
        return _result("blocked_needs_source_lock", ["source_reference_not_locked"], source_status)
    if observation_type == "visual_cuneiform_candidate":
        blockers.extend(_visual_blockers(decision))
        if not decision.get("accepted_reading"):
            blockers.append("cuneiform_reading_not_accepted")
        category = "blocked_needs_coordinates" if "coordinates_required" in blockers else "blocked_needs_human_review"
        return _result(category, blockers, source_status)
    if observation_type == "visual_dot_pattern_candidate":
        blockers.extend(_visual_blockers(decision))
        blockers.append("dot_reading_ambiguous_or_unforced")
        return _result("quarantined_false_positive", blockers, source_status)
    if observation_type == "delimiter_candidate":
        return _result("blocked_needs_human_review", ["delimiter_meaning_not_reviewed"], source_status)
    if observation_type == "cookie_hash_candidate":
        return _result("blocked_negative_result", ["stage4g_exact_cookie_refresh_zero_matches"], source_status)
    if observation_type == "stego_audio_fixture_candidate":
        return _result(
            "blocked_toolchain_unavailable",
            ["toolchain_unavailable", "expected_output_hash_missing"],
            source_status,
        )
    if observation_type == "image_compression_artifact_candidate":
        return _result("deferred", ["source_variant_preflight_required"], source_status)
    if observation_type == "discord_derived_lead":
        if not decision.get("public_source_corroboration"):
            blockers.append("public_source_corroboration_required")
        if not _is_locked(source_status):
            blockers.append("source_lock_required")
        blockers.append("needs_human_review")
        category = "blocked_needs_source_lock" if "source_lock_required" in blockers else "blocked_needs_human_review"
        return _result(category, blockers, source_status)
    if not _is_locked(source_status):
        return _result("blocked_needs_source_lock", ["source_lock_required"], source_status)
    if review_state in {"needs_human_review", "pending"}:
        return _result("blocked_needs_human_review", ["needs_human_review"], source_status)
    if review_state in {"deferred", "needs_source_lock"}:
        return _result("deferred", [f"review_state_{review_state}"], source_status)
    if review_state in {"accepted", "promoted_to_manifest"} and decision.get("usable_as_experiment_seed") is True:
        return _result("ready_for_manifest", [], source_status, usable_as_experiment_seed=True)
    return _result("blocked_needs_human_review", ["explicit_promotion_not_requested"], source_status)


def _visual_blockers(decision: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    if not decision.get("has_page_or_image_reference"):
        blockers.append("page_or_image_reference_required")
    if not decision.get("has_coordinates"):
        blockers.append("coordinates_required")
    if decision.get("ambiguous") is True:
        blockers.append("ambiguous_reading")
    return blockers


def _source_lock_status(decision: dict[str, Any], source_lock: dict[str, Any] | None) -> str | None:
    if source_lock is not None:
        return str(source_lock.get("lock_status") or "")
    if decision.get("source_locked") is True:
        return "source_locked"
    return None


def _is_locked(source_status: str | None) -> bool:
    return bool(source_status in LOCKED_SOURCE_STATUSES)


def _result(
    category: str,
    blockers: list[str],
    source_status: str | None,
    *,
    usable_as_experiment_seed: bool = False,
) -> dict[str, Any]:
    return {
        "promotion_category": category,
        "blockers": list(dict.fromkeys(blockers)),
        "source_lock_status": source_status,
        "usable_as_experiment_seed": usable_as_experiment_seed,
    }
