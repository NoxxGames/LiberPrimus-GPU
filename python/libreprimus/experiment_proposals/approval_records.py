"""Approval record loading and validation for Stage 2G."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from libreprimus.experiment_proposals.models import ApprovalRecord, ExperimentProposal
from libreprimus.experiment_proposals.validation import validate_payload
from libreprimus.paths import repo_root
from libreprimus.transforms.registry import compute_sha256


def load_approval_record(path: Path) -> ApprovalRecord:
    resolved = path if path.is_absolute() else repo_root() / path
    payload = load_yaml_payload(resolved)
    validate_approval_record_payload(payload)
    return ApprovalRecord(payload=payload, path=str(resolved), sha256=compute_sha256(resolved))


def load_yaml_payload(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Approval record must be a YAML mapping: {path}")
    return payload


def validate_approval_record_payload(
    payload: dict[str, Any],
    *,
    proposal: ExperimentProposal | None = None,
    now: datetime | None = None,
) -> None:
    validate_payload(payload, "experiment-approval-record-v0.schema.json")
    for field in ["canonical_corpus_active", "page_boundaries_final", "trusted_as_canonical"]:
        if payload.get(field) is not False:
            raise ValueError(f"Approval records require {field}=false.")
    status = payload.get("approval_status")
    if status != "approved":
        if payload.get("approved_for_execution") is not False:
            raise ValueError("Non-approved approval records must have approved_for_execution=false.")
        return

    if payload.get("approved_for_execution") is not True:
        raise ValueError("Approved records require approved_for_execution=true.")
    for field in ["approved_by", "approved_at_utc", "expiry_utc"]:
        if not str(payload.get(field, "")).strip():
            raise ValueError(f"Approved records require non-empty {field}.")
    if not isinstance(payload.get("approval_scope"), dict) or not payload["approval_scope"]:
        raise ValueError("Approved records require a non-empty approval_scope.")
    if not isinstance(payload.get("constraints"), list) or not payload["constraints"]:
        raise ValueError("Approved records require constraints.")
    expiry = _parse_utc(str(payload["expiry_utc"]))
    current = now or datetime.now(UTC)
    if expiry <= current:
        raise ValueError("Approved record is expired.")
    if proposal is not None:
        if payload.get("proposal_id") != proposal.proposal_id:
            raise ValueError("Approval record proposal_id does not match proposal.")
        if payload.get("proposal_sha256") != proposal.sha256:
            raise ValueError("Approval record proposal_sha256 does not match proposal.")
        scope = payload["approval_scope"]
        if scope.get("proposal_id") != proposal.proposal_id:
            raise ValueError("Approval scope does not match proposal.")


def _parse_utc(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=UTC)

