"""Review checklist helpers for Stage 2G proposals."""

from __future__ import annotations

from typing import Any

from libreprimus.experiment_proposals.validation import validate_payload


def validate_review_checklist(payload: dict[str, Any], *, proposal_id: str) -> None:
    validate_payload(payload, "experiment-review-checklist-v0.schema.json")
    if payload.get("proposal_id") != proposal_id:
        raise ValueError("Review checklist proposal_id does not match proposal.")


def checklist_summary(payload: dict[str, Any]) -> dict[str, int]:
    items = payload.get("items", [])
    return {
        "item_count": len(items),
        "pass_count": sum(1 for item in items if item.get("status") == "pass"),
        "pending_count": sum(1 for item in items if item.get("status") == "pending"),
        "fail_count": sum(1 for item in items if item.get("status") == "fail"),
        "blocking_count": len(payload.get("blocking_items", [])),
    }

