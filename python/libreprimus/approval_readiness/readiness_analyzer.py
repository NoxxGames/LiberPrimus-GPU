"""Analyze Stage 2I proposals for human approval readiness."""

from __future__ import annotations

from pathlib import Path

from libreprimus.approval_readiness.models import ReadinessAnalysis
from libreprimus.experiment_proposals.approval_records import load_approval_record
from libreprimus.experiment_proposals.models import ApprovalRecord
from libreprimus.experiment_proposals.models import ExperimentProposal
from libreprimus.experiment_proposals.proposal_loader import load_experiment_proposal
from libreprimus.paths import repo_root


def analyze_approval_readiness(
    proposal_path: Path,
    *,
    approval_path: Path | None = None,
) -> ReadinessAnalysis:
    proposal = load_experiment_proposal(_resolve_path(proposal_path))
    approval = load_approval_record(_resolve_path(approval_path)) if approval_path is not None else None
    payload = proposal.payload
    corpus_slice = payload.get("corpus_slice", {})
    real_unsolved = isinstance(corpus_slice, dict) and corpus_slice.get("slice_kind") in {
        "future_unsolved_page_candidate",
        "page_candidate",
    }
    approval_status = "missing" if approval is None else str(approval.payload.get("approval_status", "unknown"))
    candidate_estimate = int(payload.get("candidate_count_estimate", 0))
    candidate_upper = int(payload.get("candidate_count_upper_bound", 0))
    blocking = _blocking_conditions(proposal, approval, real_unsolved)
    warnings = []
    if real_unsolved:
        warnings.append("real_unsolved_metadata_requires_separate_human_approval")
    if candidate_estimate != candidate_upper:
        warnings.append("candidate_estimate_differs_from_upper_bound")
    status = "invalid" if _has_invalid_blocker(blocking) else "blocked_pending_approval"
    if approval_status in {"missing", "pending"} and not _has_invalid_blocker(blocking):
        status = "ready_for_human_review"
    return ReadinessAnalysis(
        proposal=proposal,
        approval=approval,
        readiness_status=status,
        approval_status=approval_status,
        real_unsolved_material_touched=real_unsolved,
        candidate_count_estimate=candidate_estimate,
        candidate_count_upper_bound=candidate_upper,
        blocking_conditions=blocking,
        warnings=warnings,
    )


def _blocking_conditions(
    proposal: ExperimentProposal,
    approval: ApprovalRecord | None,
    real_unsolved: bool,
) -> list[str]:
    payload = proposal.payload
    blocking = [
        "explicit_approved_approval_record_required_before_execution",
        "separate_human_decision_required",
    ]
    if approval is None:
        blocking.append("approval_record_missing")
    elif approval.payload.get("approval_status") != "pending":
        blocking.append("stage2i_approval_status_must_remain_pending")
    if approval is not None and approval.payload.get("approved_for_execution") is not False:
        blocking.append("approval_record_must_not_approve_execution")
    if payload.get("proposal_status") != "ready_for_review":
        blocking.append("proposal_status_not_ready_for_review")
    if payload.get("candidate_count_estimate") != 841 or payload.get("candidate_count_upper_bound") != 841:
        blocking.append("candidate_count_bound_must_be_841")
    if not real_unsolved:
        blocking.append("proposal_must_touch_reviewable_unsolved_metadata")
    if payload.get("review_checklist", {}).get("items") is None:
        blocking.append("review_checklist_missing")
    for field in [
        "approved_for_execution",
        "execution_enabled",
        "search_execution_enabled",
        "candidate_generation_enabled",
        "scoring_enabled",
        "cuda_enabled",
        "canonical_corpus_active",
        "page_boundaries_final",
        "trusted_as_canonical",
    ]:
        if payload.get(field) is not False:
            blocking.append(f"{field}_must_be_false")
    return blocking


def _has_invalid_blocker(blocking: list[str]) -> bool:
    allowed = {
        "explicit_approved_approval_record_required_before_execution",
        "separate_human_decision_required",
        "approval_record_missing",
    }
    return any(item not in allowed for item in blocking)


def _resolve_path(path: Path | None) -> Path:
    if path is None:
        raise ValueError("Path is required.")
    return path if path.is_absolute() else repo_root() / path
