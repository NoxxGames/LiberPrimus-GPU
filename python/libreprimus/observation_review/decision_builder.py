"""Build Stage 4J observation-review decisions."""

from __future__ import annotations

from typing import Any

from libreprimus.observation_review.models import ObservationInput
from libreprimus.observation_review.promotion_gates import promotion_blocked_reasons


def build_review_decisions(inputs: list[ObservationInput]) -> list[dict[str, Any]]:
    """Return deterministic review decisions for normalized observation inputs."""

    decisions = [_build_decision(item) for item in inputs]
    for decision in decisions:
        decision["promotion_blocked_reasons"] = promotion_blocked_reasons(decision)
    return sorted(decisions, key=lambda record: record["review_decision_id"])


def _build_decision(item: ObservationInput) -> dict[str, Any]:
    payload = item.payload
    observation_type = item.observation_type
    review_state = _review_state(item)
    page_refs = payload.get("page_refs") if isinstance(payload.get("page_refs"), list) else []
    image_refs = payload.get("image_refs") if isinstance(payload.get("image_refs"), list) else []
    annotation_status = str(payload.get("annotation_status") or "")
    source_locked = _source_locked(item)
    has_coordinates = _has_coordinates(payload)
    has_page_or_image_reference = bool(page_refs or image_refs)
    decision = {
        "record_type": "observation_review_decision",
        "review_decision_id": f"stage4j-decision-{item.source_family}-{item.observation_id}",
        "observation_id": item.observation_id,
        "source_family": item.source_family,
        "source_path": item.source_path,
        "observation_type": observation_type,
        "review_state": review_state,
        "reviewed_by": "automated_policy_check",
        "source_locked": source_locked,
        "public_source_corroboration": bool(payload.get("public_source_corroboration") or source_locked),
        "has_page_or_image_reference": has_page_or_image_reference,
        "has_coordinates": has_coordinates,
        "accepted_reading": False,
        "ambiguous": _ambiguous(item),
        "annotation_status": annotation_status or None,
        "false_positive_class": payload.get("false_positive_class") or payload.get("observation_family"),
        "why_dangerous": payload.get("why_dangerous"),
        "rationale": _rationale(item, review_state),
        "solve_claim": False,
        "trusted_as_canonical": False,
        "usable_as_experiment_seed": False,
    }
    if observation_type in {"source_link", "negative_control"}:
        decision["public_source_corroboration"] = bool(source_locked)
    return decision


def _review_state(item: ObservationInput) -> str:
    payload = item.payload
    observation_type = item.observation_type
    if observation_type == "visual_cuneiform_candidate":
        return "needs_coordinates"
    if observation_type == "visual_dot_pattern_candidate":
        if "negative" in str(payload.get("review_status") or "").lower() or "dot" in item.source_family:
            return "quarantined"
        return "needs_human_review"
    if observation_type == "delimiter_candidate":
        return "needs_human_review"
    if observation_type == "negative_control":
        return "negative_control"
    if observation_type == "source_link":
        return "accepted" if _source_locked(item) else "needs_source_lock"
    if observation_type == "cookie_hash_candidate":
        if int(payload.get("exact_match_count") or 0) == 0 and "summary" in item.source_family:
            return "rejected"
        return "deferred"
    if observation_type == "stego_audio_fixture_candidate":
        return "deferred"
    if observation_type == "image_compression_artifact_candidate":
        return "deferred"
    if observation_type == "discord_derived_lead":
        return "needs_source_lock"
    if observation_type in {"numeric_claim", "gp_rune_claim"}:
        return "needs_source_lock"
    return "pending"


def _source_locked(item: ObservationInput) -> bool:
    payload = item.payload
    if item.source_family == "stage4b_sources":
        return True
    if "source_id" in payload and item.source_family not in {"stage3r_discord_observations"}:
        return True
    if "source_url" in payload:
        return True
    return False


def _has_coordinates(payload: dict[str, Any]) -> bool:
    if payload.get("coordinates") or payload.get("region") or payload.get("regions"):
        return True
    coordinate_system = str(payload.get("coordinate_system") or "")
    return coordinate_system in {"pixel_absolute", "normalized_0_1"} and payload.get("annotation_status") == "annotated"


def _ambiguous(item: ObservationInput) -> bool:
    payload = item.payload
    if item.observation_type == "visual_dot_pattern_candidate":
        return True
    if item.observation_type == "visual_cuneiform_candidate":
        return True
    if payload.get("ambiguity_notes"):
        return True
    return False


def _rationale(item: ObservationInput, review_state: str) -> str:
    if item.observation_type == "visual_cuneiform_candidate":
        return "Cuneiform reading remains review-required until exact coordinates and accepted readout exist."
    if item.observation_type == "visual_dot_pattern_candidate":
        return "Dot readings remain ambiguous and unforced; use as review/quarantine material, not seeds."
    if item.observation_type == "delimiter_candidate":
        return "Delimiter observations need human review before any handedness or reset metadata can be inferred."
    if item.observation_type == "negative_control":
        return "Negative-control class is useful as a control without truth acceptance."
    if item.observation_type == "cookie_hash_candidate" and review_state == "rejected":
        return "Stage 4G exact source-backed cookie refresh produced zero exact matches."
    if item.observation_type == "source_link" and review_state == "accepted":
        return "Promoted source reference is source-locked as reference metadata, not canonical plaintext."
    if item.observation_type == "stego_audio_fixture_candidate":
        return "Fixture candidate remains deferred until assets and documented toolchain are available."
    if item.observation_type == "image_compression_artifact_candidate":
        return "Image artifact observations require future source-variant preflight and controls."
    return "Automated Stage 4J policy review prevents implicit promotion."
