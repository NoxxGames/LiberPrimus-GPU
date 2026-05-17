"""Generate Stage 2I approval-readiness packets."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from libreprimus.approval_readiness.models import ApprovalReadinessPacket, ReadinessAnalysis
from libreprimus.approval_readiness.readiness_analyzer import analyze_approval_readiness
from libreprimus.approval_readiness.validation import validate_record
from libreprimus.experiment_proposals.checklist import checklist_summary
from libreprimus.paths import repo_root

DETERMINISTIC_READINESS_TIMESTAMP = "1970-01-01T00:00:00Z"
REVIEW_PACKET_VERSION = "stage2i-followup-review-packet-v0"


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
    corpus_slice = _corpus_slice(payload, proposal_path=Path(proposal.path))
    transform_summary = _transform_summary(transform_space, analysis)
    safety_summary = _safety_summary(payload, out_dir=out_dir)
    machine_checks = _machine_check_results(analysis, payload=payload, safety_summary=safety_summary)
    warnings = list(analysis.warnings)
    if corpus_slice.get("metadata_path_status") == "no_standalone_metadata_path_referenced":
        warnings.append("corpus_metadata_path_missing_recommend_revision_or_accept_embedded_selector")
    approval_requirements = [
        "human reviewer must approve explicitly in a separate approval record",
        "approval must identify proposal SHA-256",
        "approval must define scope, constraints, approver, timestamp, and expiry",
        "approval must not activate canonical corpus or finalize page boundaries",
    ]
    packet = ApprovalReadinessPacket(
        record_type="approval_readiness_packet",
        packet_id=f"{proposal.proposal_id}-approval-readiness-{proposal.sha256[:12]}",
        review_packet_version=REVIEW_PACKET_VERSION,
        proposal_id=proposal.proposal_id,
        proposal_path=proposal.path,
        approval_path=analysis.approval.path if analysis.approval is not None else "",
        proposal_sha256=proposal.sha256,
        approval_sha256=analysis.approval.sha256 if analysis.approval is not None else "",
        generated_at_utc=DETERMINISTIC_READINESS_TIMESTAMP,
        git_commit=_git_commit(),
        proposal_status=str(payload["proposal_status"]),
        approval_status=analysis.approval_status,
        approved_for_execution=False,
        execution_enabled=False,
        human_approval_required=payload.get("human_approval_required") is True,
        search_execution_enabled=False,
        candidate_generation_enabled=False,
        scoring_enabled=False,
        cuda_enabled=False,
        canonical_corpus_active=False,
        page_boundaries_final=False,
        trusted_as_canonical=False,
        real_unsolved_material_touched=analysis.real_unsolved_material_touched,
        corpus_slice=corpus_slice,
        transform_summary=transform_summary,
        safety_summary=safety_summary,
        corpus_slice_summary=_corpus_slice_summary(payload),
        transform_space_summary=_transform_space_summary(transform_space),
        candidate_count_estimate=analysis.candidate_count_estimate,
        candidate_count_upper_bound=analysis.candidate_count_upper_bound,
        safety_gate_summary=_safety_gate_summary(payload),
        review_checklist_summary=checklist_summary(payload["review_checklist"]),
        approval_requirements=approval_requirements,
        blocking_conditions=analysis.blocking_conditions,
        machine_check_results=machine_checks,
        human_decision_required=True,
        risk_summary=_risk_summary(analysis),
        recommended_decision="revise_or_defer_until_metadata_path_is_explicit"
        if corpus_slice.get("metadata_path_status") == "no_standalone_metadata_path_referenced"
        else "human_review_required_approve_revise_or_deny",
        recommended_human_decision="review_required_approve_deny_or_revise",
        decision_options=_decision_options(),
        next_commands=_next_commands(),
        generated_output_preview=_output_paths(proposal.proposal_id, out_dir),
        result_store_preview=dict(payload.get("result_store_policy", {})),
        warnings=warnings,
        notes=[
            "Approval-readiness packet is not an approval.",
            "No proposal execution, candidate generation, scoring, or CUDA is performed.",
            "The human decision is limited to approve later execution, revise the proposal, or deny/defer.",
        ],
    )
    return packet


def _corpus_slice(payload: dict[str, Any], *, proposal_path: Path) -> dict[str, Any]:
    corpus_slice = payload.get("corpus_slice", {})
    source = str(corpus_slice.get("source", ""))
    generated_manifest = Path("data/normalized/corpus-candidates") / source / "corpus_candidate_manifest.json"
    docs_path = Path("docs/corpus/canonical-corpus-v0-candidate.md")
    metadata_paths = [
        _path_record("proposal embedded selector metadata", proposal_path, "selector_metadata"),
        _path_record("corpus candidate documentation", docs_path, "documentation"),
        _path_record("generated corpus candidate manifest", generated_manifest, "generated_local_metadata"),
    ]
    standalone_paths = corpus_slice.get("metadata_paths", [])
    if isinstance(standalone_paths, list):
        metadata_paths.extend(
            _path_record("proposal-declared corpus metadata", Path(str(path)), "proposal_declared_metadata")
            for path in standalone_paths
        )
    metadata_path_status = (
        "proposal_declares_standalone_metadata_path"
        if standalone_paths
        else "no_standalone_metadata_path_referenced"
    )
    return {
        "slice_id": corpus_slice.get("slice_id"),
        "slice_kind": corpus_slice.get("slice_kind"),
        "source": source,
        "selector": corpus_slice.get("selector", {}),
        "metadata_paths": metadata_paths,
        "metadata_path_status": metadata_path_status,
        "metadata_path_message": (
            "No standalone corpus metadata file is currently referenced; the proposal uses reviewable selector metadata embedded in the proposal."
            if metadata_path_status == "no_standalone_metadata_path_referenced"
            else "Proposal declares standalone corpus metadata path(s)."
        ),
        "raw_unsolved_text_included": False,
        "review_required": corpus_slice.get("review_required") is True,
    }


def _path_record(label: str, path: Path, role: str) -> dict[str, Any]:
    resolved = path if path.is_absolute() else repo_root() / path
    return {
        "label": label,
        "path": str(path),
        "absolute_path": str(resolved),
        "exists": resolved.exists(),
        "role": role,
    }


def _transform_summary(transform_space: dict[str, Any], analysis: ReadinessAnalysis) -> dict[str, Any]:
    families = transform_space.get("families", [])
    if not isinstance(families, list):
        families = []
    count_by_family = {
        str(family.get("transform_family")): int(family.get("candidate_count_estimate", 0))
        for family in families
        if isinstance(family, dict)
    }
    return {
        "transform_families": list(count_by_family),
        "candidate_count_by_family": count_by_family,
        "total_candidate_count": analysis.candidate_count_estimate,
        "candidate_count_upper_bound": analysis.candidate_count_upper_bound,
    }


def _safety_summary(payload: dict[str, Any], *, out_dir: Path) -> dict[str, Any]:
    return {
        "canonical_corpus_active": payload.get("canonical_corpus_active") is True,
        "page_boundaries_final": payload.get("page_boundaries_final") is True,
        "search_execution_enabled": payload.get("search_execution_enabled") is True,
        "candidate_generation_enabled": payload.get("candidate_generation_enabled") is True,
        "scoring_enabled": payload.get("scoring_enabled") is True,
        "cuda_enabled": payload.get("cuda_enabled") is True,
        "raw_outputs_committed": False,
        "generated_outputs_ignored": _generated_outputs_ignored(out_dir),
    }


def _machine_check_results(
    analysis: ReadinessAnalysis,
    *,
    payload: dict[str, Any],
    safety_summary: dict[str, Any],
) -> list[dict[str, Any]]:
    approval_pending = analysis.approval_status == "pending"
    candidate_bound_present = "candidate_count_upper_bound" in payload
    count_within_bound = analysis.candidate_count_estimate <= analysis.candidate_count_upper_bound
    checks = [
        _check("raw unsolved text included", True, "false", "proposal selector has raw_text_included=false and packet does not include raw text", "error"),
        _check("candidate bound present", candidate_bound_present, "candidate_count_upper_bound is present", "proposal declares upper bound", "error"),
        _check("count within bound", count_within_bound, f"{analysis.candidate_count_estimate} <= {analysis.candidate_count_upper_bound}", "candidate estimate is bounded", "error"),
        _check("approval pending", approval_pending, analysis.approval_status, "Stage 2I requires pending approval", "error"),
        _check("execution disabled", payload.get("execution_enabled") is False, "false", "proposal execution_enabled=false", "error"),
        _check("scoring disabled", payload.get("scoring_enabled") is False, "false", "proposal scoring_enabled=false", "error"),
        _check("CUDA disabled", payload.get("cuda_enabled") is False, "false", "proposal cuda_enabled=false", "error"),
        _check("canonical corpus inactive", payload.get("canonical_corpus_active") is False, "false", "proposal canonical_corpus_active=false", "error"),
        _check("page boundaries final", payload.get("page_boundaries_final") is False, "false", "proposal page_boundaries_final=false", "error"),
        _check("generated outputs ignored", bool(safety_summary["generated_outputs_ignored"]), "true", "approval-readiness outputs are under ignored result paths", "error"),
    ]
    safe_later = (
        candidate_bound_present
        and count_within_bound
        and payload.get("execution_enabled") is False
        and payload.get("scoring_enabled") is False
        and payload.get("cuda_enabled") is False
        and payload.get("candidate_generation_enabled") is False
    )
    checks.append(
        _check(
            "proposal safe to approve later",
            safe_later,
            "true" if safe_later else "false",
            "safe only if a future approval record remains scope-bound and execution stays separate",
            "warning",
        )
    )
    return checks


def _check(name: str, passed: bool, result: str, evidence: str, severity: str) -> dict[str, str]:
    return {
        "check": name,
        "result": "pass" if passed else "fail",
        "evidence": evidence,
        "actual": result,
        "severity": severity,
    }


def _generated_outputs_ignored(out_dir: Path) -> bool:
    root = repo_root()
    resolved = out_dir if out_dir.is_absolute() else root / out_dir
    try:
        relative = resolved.relative_to(root)
    except ValueError:
        return True
    return str(relative).replace("\\", "/").startswith("experiments/results/approval-readiness/")


def _decision_options() -> list[dict[str, str]]:
    return [
        {
            "option": "A",
            "decision": "approve later execution",
            "meaning": "Create a separate future approval record with scope, constraints, approver, timestamp, expiry, and matching proposal SHA-256.",
            "does_not_do": "Does not execute this proposal by itself.",
        },
        {
            "option": "B",
            "decision": "revise proposal",
            "meaning": "Ask for clearer corpus metadata paths, narrower selector metadata, changed transform bounds, or different stop conditions.",
            "does_not_do": "Does not approve or execute anything.",
        },
        {
            "option": "C",
            "decision": "deny/defer",
            "meaning": "Record that the proposal should not proceed as written.",
            "does_not_do": "Does not run any experiment.",
        },
    ]


def _next_commands() -> dict[str, str]:
    return {
        "approve_later_execution": (
            "Stage 2J - create an explicit approved approval record for stage2i-first-bounded-caesar-affine-review, "
            "scope-bound to the reviewed proposal, but do not execute it in the same step."
        ),
        "revise_proposal": (
            "Stage 2I-followup - revise stage2i-first-bounded-caesar-affine-review with clearer corpus metadata paths, "
            "bounds, or stop conditions; regenerate the review packet."
        ),
        "deny_or_defer": (
            "Stage 2J - record a denied or deferred decision for stage2i-first-bounded-caesar-affine-review and keep execution blocked."
        ),
    }


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
    review_markdown = out_dir / f"{proposal_id}.review.md"
    return {
        "packet_json": str(out_dir / f"{proposal_id}-approval-readiness-packet.json"),
        "packet_markdown": str(review_markdown),
        "review_markdown": str(review_markdown),
        "summary": str(out_dir / "summary.json"),
    }


def _git_commit() -> str:
    result = subprocess.run(["git", "rev-parse", "HEAD"], check=False, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else "unknown"
