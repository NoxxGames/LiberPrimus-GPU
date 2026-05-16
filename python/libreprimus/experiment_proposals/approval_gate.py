"""Approval gate logic for Stage 2G proposals."""

from __future__ import annotations

from libreprimus.experiment_proposals.approval_records import validate_approval_record_payload
from libreprimus.experiment_proposals.models import ApprovalGateResult, ApprovalRecord, ExperimentProposal


def evaluate_approval_gate(
    proposal: ExperimentProposal,
    approval: ApprovalRecord | None = None,
) -> ApprovalGateResult:
    if approval is None:
        return ApprovalGateResult(
            proposal_id=proposal.proposal_id,
            approval_status="missing",
            approved_for_execution=False,
            execution_blocked=True,
            reason="No approval record was provided.",
        )
    status = approval.payload.get("approval_status", "unknown")
    if status != "approved":
        return ApprovalGateResult(
            proposal_id=proposal.proposal_id,
            approval_status=str(status),
            approved_for_execution=False,
            execution_blocked=True,
            reason=f"Approval status is {status}; execution remains blocked.",
        )
    try:
        validate_approval_record_payload(approval.payload, proposal=proposal)
    except ValueError as exc:
        return ApprovalGateResult(
            proposal_id=proposal.proposal_id,
            approval_status=str(status),
            approved_for_execution=False,
            execution_blocked=True,
            reason=str(exc),
        )
    return ApprovalGateResult(
        proposal_id=proposal.proposal_id,
        approval_status="approved",
        approved_for_execution=True,
        execution_blocked=False,
        reason="Approval record is valid for this proposal.",
    )

