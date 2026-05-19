"""Build Stage 4L reviewed observation promotion ledger records."""

from __future__ import annotations

from typing import Any

from libreprimus.observation_promotion.blockers import build_blocker_records
from libreprimus.observation_promotion.gates import evaluate_decision, source_lock_for_decision
from libreprimus.observation_promotion.models import safety_flags


def build_promotion_ledger(
    decisions: list[dict[str, Any]],
    source_locks: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Build ledger, readiness, and blocker records from reviewed decisions."""

    source_lock_by_candidate = {
        str(record.get("source_candidate_id") or ""): record
        for record in source_locks
        if record.get("source_candidate_id")
    }
    ledger_records: list[dict[str, Any]] = []
    readiness_records: list[dict[str, Any]] = []
    blocker_records: list[dict[str, Any]] = []
    for decision in sorted(decisions, key=lambda item: str(item.get("review_decision_id") or "")):
        source_lock = source_lock_for_decision(decision, source_lock_by_candidate)
        gate = evaluate_decision(decision, source_lock)
        blockers = gate["blockers"]
        decision_blockers = build_blocker_records(decision, blockers)
        blocker_records.extend(decision_blockers)
        decision_id = str(decision.get("review_decision_id") or "")
        observation_id = str(decision.get("observation_id") or "")
        common = {
            "review_decision_id": decision_id,
            "observation_id": observation_id,
            "observation_type": decision.get("observation_type"),
            "review_state": decision.get("review_state"),
            "source_family": decision.get("source_family"),
            "source_path": decision.get("source_path"),
            "source_lock_status": gate["source_lock_status"],
            "source_lock_record_id": source_lock.get("snapshot_record_id") if source_lock else None,
            "promotion_category": gate["promotion_category"],
            "blockers": blockers,
            "blocker_ids": [record["blocker_record_id"] for record in decision_blockers],
            "usable_as_experiment_seed": bool(gate["usable_as_experiment_seed"]),
            **safety_flags(),
        }
        for field in (
            "source_context",
            "source_image_name",
            "source_image_sha256",
            "source_image_byte_length",
            "source_image_metadata_cache_path",
            "claimed_matrix",
            "claimed_rune_count",
            "claimed_pattern",
            "evidence_strength",
            "false_positive_risk",
            "future_bounded_verifier_candidate",
            "negative_control_note",
        ):
            if field in decision:
                common[field] = decision[field]
        ledger_records.append(
            {
                "record_type": "reviewed_observation_promotion_ledger_record",
                "ledger_record_id": f"stage4l-ledger-{decision_id}",
                **common,
            }
        )
        readiness_records.append(
            {
                "record_type": "observation_promotion_readiness_record",
                "readiness_record_id": f"stage4l-readiness-{decision_id}",
                **common,
            }
        )
    return ledger_records, readiness_records, blocker_records
