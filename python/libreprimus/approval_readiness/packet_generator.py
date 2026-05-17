"""Generate Stage 2I approval-readiness packets."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from libreprimus.approval_readiness.models import ApprovalReadinessPacket, ReadinessAnalysis
from libreprimus.approval_readiness.readiness_analyzer import analyze_approval_readiness
from libreprimus.approval_readiness.validation import validate_record
from libreprimus.experiment_proposals.checklist import checklist_summary

DETERMINISTIC_READINESS_TIMESTAMP = "1970-01-01T00:00:00Z"


def build_approval_readiness_packet(
    proposal_path: Path,
    *,
    approval_path: Path | None = None,
    out_dir: Path,
) -> ApprovalReadinessPacket:
    analysis = analyze_approval_readiness(proposal_path, approval_path=approval_path)
    packet = packet_from_analysis(analysis, out_dir=out_dir)
    validate_record(packet)
    return packet


def packet_from_analysis(analysis: ReadinessAnalysis, *, out_dir: Path) -> ApprovalReadinessPacket:
    proposal = analysis.proposal
    payload = proposal.payload
    transform_space = payload.get("transform_space", {})
    approval_requirements = [
        "human reviewer must approve explicitly in a separate approval record",
        "approval must identify proposal SHA-256",
        "approval must define scope, constraints, approver, timestamp, and expiry",
        "approval must not activate canonical corpus or finalize page boundaries",
    ]
    packet = ApprovalReadinessPacket(
        record_type="approval_readiness_packet",
        packet_id=f"{proposal.proposal_id}-approval-readiness-{proposal.sha256[:12]}",
        proposal_id=proposal.proposal_id,
        proposal_sha256=proposal.sha256,
        generated_at_utc=DETERMINISTIC_READINESS_TIMESTAMP,
        git_commit=_git_commit(),
        proposal_status=str(payload["proposal_status"]),
        approval_status=analysis.approval_status,
        approved_for_execution=False,
        execution_enabled=False,
        search_execution_enabled=False,
        candidate_generation_enabled=False,
        scoring_enabled=False,
        cuda_enabled=False,
        canonical_corpus_active=False,
        page_boundaries_final=False,
        trusted_as_canonical=False,
        real_unsolved_material_touched=analysis.real_unsolved_material_touched,
        corpus_slice_summary=_corpus_slice_summary(payload),
        transform_space_summary=_transform_space_summary(transform_space),
        candidate_count_estimate=analysis.candidate_count_estimate,
        candidate_count_upper_bound=analysis.candidate_count_upper_bound,
        safety_gate_summary=_safety_gate_summary(payload),
        review_checklist_summary=checklist_summary(payload["review_checklist"]),
        approval_requirements=approval_requirements,
        blocking_conditions=analysis.blocking_conditions,
        risk_summary=_risk_summary(analysis),
        recommended_human_decision="review_required_approve_deny_or_revise",
        generated_output_preview=_output_paths(proposal.proposal_id, out_dir),
        result_store_preview=dict(payload.get("result_store_policy", {})),
        warnings=analysis.warnings,
        notes=[
            "Approval-readiness packet is not an approval.",
            "No proposal execution, candidate generation, scoring, or CUDA is performed.",
        ],
    )
    return packet


def _corpus_slice_summary(payload: dict[str, Any]) -> dict[str, Any]:
    corpus_slice = payload.get("corpus_slice", {})
    return {
        "slice_id": corpus_slice.get("slice_id"),
        "slice_kind": corpus_slice.get("slice_kind"),
        "source": corpus_slice.get("source"),
        "corpus_candidate_id": corpus_slice.get("corpus_candidate_id"),
        "selector": corpus_slice.get("selector", {}),
        "review_required": corpus_slice.get("review_required"),
        "raw_text_included": False,
    }


def _transform_space_summary(transform_space: dict[str, Any]) -> dict[str, Any]:
    families = transform_space.get("families", [])
    return {
        "transform_space_id": transform_space.get("transform_space_id"),
        "families": families,
        "family_count": len(families) if isinstance(families, list) else 0,
        "execution_supported": transform_space.get("execution_supported", False),
        "dry_run_supported": transform_space.get("dry_run_supported", True),
    }


def _safety_gate_summary(payload: dict[str, Any]) -> dict[str, Any]:
    false_fields = [
        "approved_for_execution",
        "execution_enabled",
        "search_execution_enabled",
        "candidate_generation_enabled",
        "scoring_enabled",
        "cuda_enabled",
        "canonical_corpus_active",
        "page_boundaries_final",
        "trusted_as_canonical",
    ]
    return {
        "false_field_pass_count": sum(1 for field in false_fields if payload.get(field) is False),
        "false_field_count": len(false_fields),
        "human_approval_required": payload.get("human_approval_required") is True,
        "candidate_generation_performed": False,
        "candidate_outputs_included": False,
    }


def _risk_summary(analysis: ReadinessAnalysis) -> dict[str, Any]:
    return {
        "real_unsolved_metadata": analysis.real_unsolved_material_touched,
        "raw_unsolved_text_included": False,
        "candidate_outputs_included": False,
        "search_not_started": True,
        "scoring_not_started": True,
        "cuda_not_started": True,
        "primary_risk": "human approval could be misread as execution permission if not kept separate",
    }


def _output_paths(proposal_id: str, out_dir: Path) -> dict[str, str]:
    return {
        "packet_json": str(out_dir / f"{proposal_id}-approval-readiness-packet.json"),
        "packet_markdown": str(out_dir / f"{proposal_id}-approval-readiness-packet.md"),
        "summary": str(out_dir / "summary.json"),
    }


def _git_commit() -> str:
    result = subprocess.run(["git", "rev-parse", "HEAD"], check=False, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else "unknown"
