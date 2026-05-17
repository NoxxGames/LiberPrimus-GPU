"""Stage 2H approval gate for safe synthetic and solved-control execution."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.approval_execution.models import ApprovalExecutionRequest, ApprovalGateEvaluation
from libreprimus.experiment_proposals.approval_records import (
    load_yaml_payload as load_approval_payload,
    validate_approval_record_payload,
)
from libreprimus.experiment_proposals.models import ApprovalRecord
from libreprimus.experiment_proposals.proposal_loader import load_experiment_proposal
from libreprimus.paths import repo_root
from libreprimus.transforms.registry import compute_sha256

SAFE_EXECUTION_SCOPES = {
    "synthetic_only",
    "solved_fixture_only",
    "synthetic_and_solved_fixture_only",
}
UNSAFE_FALSE_FIELDS = [
    "search_execution_enabled",
    "candidate_generation_enabled",
    "scoring_enabled",
    "cuda_enabled",
    "canonical_corpus_active",
    "page_boundaries_final",
    "trusted_as_canonical",
]


def evaluate_approval_execution_gate(request: ApprovalExecutionRequest) -> ApprovalGateEvaluation:
    proposal = load_experiment_proposal(_resolve_request_path(str(request.payload["proposal_path"])))
    approval = _load_approval_record_unchecked(_resolve_request_path(str(request.payload["approval_record_path"])))
    reasons: list[str] = []
    warnings: list[str] = []
    gates: list[dict[str, Any]] = []

    def add_gate(gate_id: str, ok: bool, message: str) -> None:
        gates.append(
            {
                "gate_id": gate_id,
                "gate_name": gate_id.replace("_", " "),
                "required_value": True,
                "actual_value": ok,
                "status": "pass" if ok else "fail",
                "severity": "info" if ok else "error",
                "message": message,
            }
        )
        if not ok:
            reasons.append(message)

    request_scope = request.execution_scope
    proposal_scope = str(proposal.payload.get("execution_scope", ""))
    approval_scope = approval.payload.get("approval_scope", {})
    approval_execution_scope = _approval_execution_scope(approval_scope)
    corpus_slice = proposal.payload.get("corpus_slice", {})
    slice_kind = corpus_slice.get("slice_kind") if isinstance(corpus_slice, dict) else None

    try:
        validate_approval_record_payload(approval.payload, proposal=proposal)
        approval_record_valid = True
    except ValueError as exc:
        approval_record_valid = False
        reasons.append(str(exc))
    add_gate("approval_record_valid", approval_record_valid, "Approval record must be approved, current, scoped, and match proposal SHA.")

    add_gate(
        "approved_for_execution",
        approval.payload.get("approval_status") == "approved" and approval.payload.get("approved_for_execution") is True,
        "Approval record must explicitly approve execution.",
    )
    add_gate(
        "scope_safe",
        request_scope in SAFE_EXECUTION_SCOPES and proposal_scope in SAFE_EXECUTION_SCOPES,
        "Stage 2H execution is limited to synthetic and solved-control scopes.",
    )
    add_gate(
        "scope_matches",
        bool(approval_execution_scope) and request_scope == proposal_scope == approval_execution_scope,
        "Request, proposal, and approval scope must match exactly.",
    )
    add_gate(
        "proposal_not_future_unsolved",
        slice_kind != "future_unsolved_page_candidate",
        "Future unsolved page candidate proposals cannot execute in Stage 2H.",
    )
    add_gate(
        "proposal_not_page_candidate",
        slice_kind != "page_candidate" or corpus_slice.get("solved_fixture_only") is True,
        "Page candidate proposals must be solved-fixture-only to execute.",
    )
    for field in UNSAFE_FALSE_FIELDS:
        add_gate(
            f"{field}_false",
            proposal.payload.get(field) is False and request.payload.get(field) is False,
            f"{field} must remain false.",
        )
    add_gate(
        "unsolved_execution_disabled",
        request.payload.get("unsolved_execution_allowed") is False,
        "Unsolved execution must remain disabled.",
    )
    add_gate(
        "approval_not_for_unsolved",
        not _approval_constraints_look_unsolved_approved(approval.payload),
        "Approved records must not authorize unsolved-page execution.",
    )

    manifest_path = proposal.payload.get("execution_manifest_path")
    if not manifest_path and request_scope in SAFE_EXECUTION_SCOPES:
        warnings.append("Proposal has no execution_manifest_path; execution bridge cannot run it.")
    add_gate(
        "execution_manifest_declared",
        request_scope == "no_op_review_only" or bool(manifest_path),
        "Approved safe proposals must declare a Stage 2F execution manifest path.",
    )

    status = "pass" if not reasons and request_scope in SAFE_EXECUTION_SCOPES else "blocked"
    return ApprovalGateEvaluation(
        request=request,
        proposal=proposal,
        approval=approval,
        approval_gate_status=status,
        approved_for_execution=status == "pass",
        blocking_reasons=reasons,
        safety_gate_results=gates,
        execution_manifest_path=str(manifest_path) if manifest_path else None,
        warnings=warnings,
    )


def _resolve_request_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root() / path


def _load_approval_record_unchecked(path: Path) -> ApprovalRecord:
    payload = load_approval_payload(path)
    return ApprovalRecord(payload=payload, path=str(path), sha256=compute_sha256(path))


def _approval_execution_scope(approval_scope: Any) -> str:
    if isinstance(approval_scope, dict):
        return str(approval_scope.get("execution_scope", ""))
    if isinstance(approval_scope, str):
        return approval_scope
    return ""


def _approval_constraints_look_unsolved_approved(payload: dict[str, Any]) -> bool:
    scope_text = str(payload.get("approval_scope", "")).lower()
    return "unsolved" in scope_text
