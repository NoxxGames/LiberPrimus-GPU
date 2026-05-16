from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import yaml

from libreprimus.experiment_proposals.approval_gate import evaluate_approval_gate
from libreprimus.experiment_proposals.models import ApprovalRecord
from libreprimus.experiment_proposals.proposal_loader import load_experiment_proposal

REPO = Path(__file__).resolve().parents[2]
PROPOSAL = REPO / "experiments/proposals/stage2g/stage2g-caesar-page-candidate-proposal.yaml"
PROPOSAL_DIR = REPO / "experiments/proposals/stage2g"
PENDING = REPO / "experiments/proposals/stage2g/approval-records/stage2g-example-pending-approval.yaml"
DENIED = REPO / "experiments/proposals/stage2g/approval-records/stage2g-example-denied-approval.yaml"


def _record(payload: dict) -> ApprovalRecord:
    return ApprovalRecord(payload=payload, path="synthetic", sha256="synthetic")


def test_no_approval_means_blocked() -> None:
    proposal = load_experiment_proposal(PROPOSAL)
    gate = evaluate_approval_gate(proposal)

    assert gate.execution_blocked is True
    assert gate.approved_for_execution is False


def test_pending_approval_means_blocked() -> None:
    proposal = load_experiment_proposal(PROPOSAL)
    gate = evaluate_approval_gate(proposal, _record(yaml.safe_load(PENDING.read_text(encoding="utf-8"))))

    assert gate.execution_blocked is True
    assert gate.approval_status == "pending"


def test_denied_approval_means_blocked() -> None:
    proposal = load_experiment_proposal(PROPOSAL)
    gate = evaluate_approval_gate(proposal, _record(yaml.safe_load(DENIED.read_text(encoding="utf-8"))))

    assert gate.execution_blocked is True
    assert gate.approval_status == "denied"


def test_invalid_approval_means_blocked() -> None:
    proposal = load_experiment_proposal(PROPOSAL)
    payload = yaml.safe_load(PENDING.read_text(encoding="utf-8"))
    payload.update({"approval_status": "approved", "approved_for_execution": True})

    gate = evaluate_approval_gate(proposal, _record(payload))

    assert gate.execution_blocked is True
    assert "Approved records require" in gate.reason


def test_valid_synthetic_approved_approval_can_pass() -> None:
    proposal = load_experiment_proposal(PROPOSAL)
    payload = deepcopy(yaml.safe_load(PENDING.read_text(encoding="utf-8")))
    payload.update(
        {
            "approval_status": "approved",
            "approved_for_execution": True,
            "proposal_sha256": proposal.sha256,
            "approved_by": "unit-test-reviewer",
            "approved_at_utc": "2026-05-17T00:00:00Z",
            "approval_scope": {"proposal_id": proposal.proposal_id},
            "constraints": ["synthetic approval gate unit test"],
            "expiry_utc": "2099-01-01T00:00:00Z",
        }
    )

    gate = evaluate_approval_gate(proposal, _record(payload))

    assert gate.execution_blocked is False
    assert gate.approved_for_execution is True


def test_committed_stage2g_proposals_remain_blocked() -> None:
    for proposal_path in PROPOSAL_DIR.glob("*.yaml"):
        proposal = load_experiment_proposal(proposal_path)
        assert evaluate_approval_gate(proposal).execution_blocked is True

