from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path

import pytest
import yaml

from libreprimus.experiment_proposals.approval_records import validate_approval_record_payload
from libreprimus.experiment_proposals.proposal_loader import load_experiment_proposal

REPO = Path(__file__).resolve().parents[2]
PROPOSAL = REPO / "experiments/proposals/stage2g/stage2g-caesar-page-candidate-proposal.yaml"
PENDING = REPO / "experiments/proposals/stage2g/approval-records/stage2g-example-pending-approval.yaml"
DENIED = REPO / "experiments/proposals/stage2g/approval-records/stage2g-example-denied-approval.yaml"


def _pending() -> dict:
    return yaml.safe_load(PENDING.read_text(encoding="utf-8"))


def _approved_payload() -> dict:
    proposal = load_experiment_proposal(PROPOSAL)
    payload = deepcopy(_pending())
    payload.update(
        {
            "approval_id": "synthetic-approved",
            "proposal_sha256": proposal.sha256,
            "approval_status": "approved",
            "approved_for_execution": True,
            "approved_by": "unit-test-reviewer",
            "approved_at_utc": "2026-05-17T00:00:00Z",
            "approval_scope": {"proposal_id": proposal.proposal_id},
            "constraints": ["synthetic unit test only"],
            "expiry_utc": "2099-01-01T00:00:00Z",
        }
    )
    return payload


def test_pending_approval_record_validates() -> None:
    validate_approval_record_payload(_pending())


def test_denied_approval_record_validates() -> None:
    validate_approval_record_payload(yaml.safe_load(DENIED.read_text(encoding="utf-8")))


def test_approved_record_without_approved_by_fails() -> None:
    payload = _approved_payload()
    payload["approved_by"] = ""

    with pytest.raises(ValueError, match="approved_by"):
        validate_approval_record_payload(payload)


def test_approved_record_without_expiry_fails() -> None:
    payload = _approved_payload()
    payload["expiry_utc"] = ""

    with pytest.raises(ValueError, match="expiry"):
        validate_approval_record_payload(payload)


def test_approved_record_with_mismatched_proposal_hash_fails() -> None:
    proposal = load_experiment_proposal(PROPOSAL)
    payload = _approved_payload()
    payload["proposal_sha256"] = "0" * 64

    with pytest.raises(ValueError, match="proposal_sha256"):
        validate_approval_record_payload(payload, proposal=proposal)


def test_expired_approval_fails() -> None:
    payload = _approved_payload()
    payload["expiry_utc"] = "2000-01-01T00:00:00Z"

    with pytest.raises(ValueError, match="expired"):
        validate_approval_record_payload(payload, now=datetime(2026, 5, 17, tzinfo=UTC))

