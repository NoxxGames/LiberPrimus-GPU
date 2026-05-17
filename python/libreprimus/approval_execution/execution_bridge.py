"""Bridge approved Stage 2H requests to the Stage 2F safe execution harness."""

from __future__ import annotations

import subprocess
from pathlib import Path

from libreprimus.approval_execution.approval_gate import evaluate_approval_execution_gate
from libreprimus.approval_execution.models import (
    ApprovalGatedExecutionPlan,
    ApprovalGatedExecutionResult,
    ApprovalGateEvaluation,
)
from libreprimus.approval_execution.request_loader import load_approval_execution_request
from libreprimus.approval_execution.validation import validate_record
from libreprimus.experiment_execution.cpu_runner import run_cpu_execution_manifest
from libreprimus.paths import repo_root

DETERMINISTIC_APPROVAL_EXECUTION_TIMESTAMP = "1970-01-01T00:00:00Z"


def build_approval_execution_plan(request_path: Path, *, out_dir: Path) -> ApprovalGatedExecutionPlan:
    request = load_approval_execution_request(request_path)
    gate = evaluate_approval_execution_gate(request)
    plan = _plan_from_gate(gate, out_dir=out_dir)
    validate_record(plan)
    return plan


def run_approval_execution_request(
    request_path: Path,
    *,
    out_dir: Path,
) -> tuple[ApprovalGatedExecutionPlan, ApprovalGatedExecutionResult]:
    request = load_approval_execution_request(request_path)
    gate = evaluate_approval_execution_gate(request)
    plan = _plan_from_gate(gate, out_dir=out_dir)
    validate_record(plan)
    if not gate.passed:
        result = _blocked_result(plan, gate)
        validate_record(result)
        return plan, result
    if request.execution_scope == "no_op_review_only":
        result = _blocked_result(plan, gate, status="skipped")
        validate_record(result)
        return plan, result

    manifest = _resolve_execution_manifest(gate.execution_manifest_path)
    _, execution_results, execution_summary = run_cpu_execution_manifest(
        manifest,
        out_dir=_stage2f_bridge_out_dir(),
    )
    status = "pass" if not execution_summary.get("fail_count") and not execution_summary.get("error_count") else "fail"
    result = ApprovalGatedExecutionResult(
        record_type="approval_gated_execution_result",
        result_id=f"{plan.request_id}-result",
        plan_id=plan.plan_id,
        request_id=plan.request_id,
        proposal_id=plan.proposal_id,
        approval_id=plan.approval_id,
        generated_at_utc=plan.generated_at_utc,
        git_commit=plan.git_commit,
        execution_scope=plan.execution_scope,
        execution_performed=True,
        execution_status=status,
        underlying_execution_result_ids=[item.result_id for item in execution_results],
        summary={
            "underlying_manifest_id": execution_summary.get("manifest_id"),
            "underlying_result_count": execution_summary.get("result_count", 0),
            "underlying_pass_count": execution_summary.get("pass_count", 0),
            "underlying_fail_count": execution_summary.get("fail_count", 0),
            "underlying_error_count": execution_summary.get("error_count", 0),
            "approval_gate_status": plan.approval_gate_status,
        },
        search_performed=False,
        candidate_generation_performed=False,
        scoring_used=False,
        cuda_used=False,
        unsolved_execution_allowed=False,
        canonical_corpus_active=False,
        page_boundaries_final=False,
        trusted_as_canonical=False,
        warnings=list(plan.warnings),
        elapsed_ms=0.0,
    )
    validate_record(result)
    return plan, result


def _plan_from_gate(gate: ApprovalGateEvaluation, *, out_dir: Path) -> ApprovalGatedExecutionPlan:
    request = gate.request
    proposal = gate.proposal
    approval = gate.approval
    request_id = request.request_id
    plan = ApprovalGatedExecutionPlan(
        record_type="approval_gated_execution_plan",
        plan_id=f"{request_id}-approval-execution-plan-{request.sha256[:12]}",
        request_id=request_id,
        proposal_id=proposal.proposal_id,
        proposal_sha256=proposal.sha256,
        approval_id=str(approval.payload.get("approval_id", "")),
        approval_status=str(approval.payload.get("approval_status", "")),
        approved_for_execution=gate.approved_for_execution,
        execution_scope=request.execution_scope,
        generated_at_utc=DETERMINISTIC_APPROVAL_EXECUTION_TIMESTAMP,
        git_commit=_git_commit(),
        approval_gate_status=gate.approval_gate_status,
        blocking_reasons=gate.blocking_reasons,
        safety_gate_results=gate.safety_gate_results,
        execution_manifest_preview={
            "execution_manifest_path": gate.execution_manifest_path,
            "bridge": "stage2f_cpu_execution",
            "execution_permitted": gate.passed,
        },
        output_paths=_output_paths(request_id, out_dir),
        unsolved_execution_allowed=False,
        search_execution_enabled=False,
        candidate_generation_enabled=False,
        scoring_enabled=False,
        cuda_enabled=False,
        canonical_corpus_active=False,
        page_boundaries_final=False,
        trusted_as_canonical=False,
        warnings=gate.warnings,
    )
    return plan


def _blocked_result(
    plan: ApprovalGatedExecutionPlan,
    gate: ApprovalGateEvaluation,
    *,
    status: str = "blocked",
) -> ApprovalGatedExecutionResult:
    return ApprovalGatedExecutionResult(
        record_type="approval_gated_execution_result",
        result_id=f"{plan.request_id}-result",
        plan_id=plan.plan_id,
        request_id=plan.request_id,
        proposal_id=plan.proposal_id,
        approval_id=plan.approval_id,
        generated_at_utc=plan.generated_at_utc,
        git_commit=plan.git_commit,
        execution_scope=plan.execution_scope,
        execution_performed=False,
        execution_status=status,
        underlying_execution_result_ids=[],
        summary={
            "approval_gate_status": plan.approval_gate_status,
            "blocking_reasons": list(gate.blocking_reasons),
            "underlying_result_count": 0,
        },
        search_performed=False,
        candidate_generation_performed=False,
        scoring_used=False,
        cuda_used=False,
        unsolved_execution_allowed=False,
        canonical_corpus_active=False,
        page_boundaries_final=False,
        trusted_as_canonical=False,
        warnings=list(plan.warnings),
        elapsed_ms=0.0,
    )


def _resolve_execution_manifest(value: str | None) -> Path:
    if not value:
        raise ValueError("Approval-gated execution has no safe execution manifest path.")
    path = Path(value)
    return path if path.is_absolute() else repo_root() / path


def _output_paths(request_id: str, out_dir: Path) -> dict[str, str]:
    return {
        "plan": str(out_dir / f"{request_id}-plan.json"),
        "result": str(out_dir / f"{request_id}-result.json"),
        "summary": str(out_dir / "summary.json"),
    }


def _stage2f_bridge_out_dir() -> Path:
    return repo_root() / "experiments/results/approval-gated-execution/stage2h"


def _git_commit() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else "unknown"
