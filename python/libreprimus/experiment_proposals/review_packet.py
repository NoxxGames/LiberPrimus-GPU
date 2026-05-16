"""Generate Stage 2G human review packets."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from libreprimus.experiment_proposals.approval_gate import evaluate_approval_gate
from libreprimus.experiment_proposals.checklist import checklist_summary
from libreprimus.experiment_proposals.models import ApprovalRecord, ExperimentProposal, ReviewPacket
from libreprimus.experiment_proposals.validation import validate_record
from libreprimus.experiments.dry_run_planner import build_dry_run_plan
from libreprimus.solved_fixtures.models import to_jsonable

DETERMINISTIC_REVIEW_TIMESTAMP = "1970-01-01T00:00:00Z"


def build_review_packet(
    proposal: ExperimentProposal,
    *,
    out_dir: Path,
    approval: ApprovalRecord | None = None,
) -> ReviewPacket:
    gate = evaluate_approval_gate(proposal, approval)
    payload = proposal.payload
    dry_run_summary = _dry_run_summary(payload, out_dir=out_dir)
    warnings = _warnings(payload, gate.execution_blocked)
    packet = ReviewPacket(
        record_type="experiment_review_packet",
        packet_id=f"{proposal.proposal_id}-review-packet-{proposal.sha256[:12]}",
        proposal_id=proposal.proposal_id,
        proposal_sha256=proposal.sha256,
        generated_at_utc=DETERMINISTIC_REVIEW_TIMESTAMP,
        git_commit=_git_commit(),
        proposal_summary={
            "title": payload["title"],
            "proposed_stage": payload["proposed_stage"],
            "proposal_status": payload["proposal_status"],
            "slice_kind": payload["corpus_slice"].get("slice_kind"),
            "transform_family": payload["transform_space"].get("transform_family"),
            "candidate_count_estimate": payload["candidate_count_estimate"],
            "candidate_count_upper_bound": payload["candidate_count_upper_bound"],
        },
        dry_run_summary=dry_run_summary,
        safety_gate_summary={
            "human_approval_required": payload["human_approval_required"],
            "execution_enabled": payload["execution_enabled"],
            "search_execution_enabled": payload["search_execution_enabled"],
            "candidate_generation_enabled": payload["candidate_generation_enabled"],
            "scoring_enabled": payload["scoring_enabled"],
            "cuda_enabled": payload["cuda_enabled"],
            "checklist": checklist_summary(payload["review_checklist"]),
            "approval_gate_reason": gate.reason,
        },
        risk_summary={
            "touches_future_unsolved_page_candidate": payload["corpus_slice"].get("slice_kind")
            == "future_unsolved_page_candidate",
            "requires_human_decision": True,
            "candidate_plaintexts_included": False,
        },
        approval_status=gate.approval_status,
        approved_for_execution=False,
        execution_blocked=True,
        warnings=warnings,
        recommended_decision="human_review_required",
        output_paths=_output_paths(proposal.proposal_id, out_dir),
        canonical_corpus_active=False,
        page_boundaries_final=False,
        trusted_as_canonical=False,
    )
    validate_record(packet)
    return packet


def _dry_run_summary(payload: dict[str, Any], *, out_dir: Path) -> dict[str, Any]:
    linked = payload.get("linked_dry_run_manifest")
    if not linked:
        return {"available": False, "reason": "No linked Stage 2E dry-run manifest."}
    try:
        plan = build_dry_run_plan(Path(str(linked)), out_dir=out_dir)
    except Exception as exc:  # noqa: BLE001 - review packets report dry-run context as a warning.
        return {"available": False, "reason": str(exc)}
    plan_payload = to_jsonable(plan)
    return {
        "available": True,
        "manifest_id": plan.manifest_id,
        "candidate_count_estimate": plan.candidate_count_estimate,
        "candidate_count_upper_bound": plan.candidate_count_upper_bound,
        "safety_gate_fail_count": sum(
            1 for gate in plan_payload["safety_gate_results"] if gate.get("status") == "fail"
        ),
    }


def _warnings(payload: dict[str, Any], execution_blocked: bool) -> list[str]:
    warnings: list[str] = []
    if execution_blocked:
        warnings.append("execution_blocked_pending_valid_human_approval")
    if payload["corpus_slice"].get("slice_kind") == "future_unsolved_page_candidate":
        warnings.append("future_unsolved_page_candidate_requires_review")
    return warnings


def _output_paths(proposal_id: str, out_dir: Path) -> dict[str, str]:
    return {
        "review_packet_json": str(out_dir / f"{proposal_id}-review-packet.json"),
        "review_packet_markdown": str(out_dir / f"{proposal_id}-review-packet.md"),
        "summary": str(out_dir / "summary.json"),
    }


def _git_commit() -> str:
    result = subprocess.run(["git", "rev-parse", "HEAD"], check=False, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else "unknown"

