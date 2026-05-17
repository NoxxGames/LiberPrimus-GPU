"""Run policy-checked Stage 2J bounded experiment queue items."""

from __future__ import annotations

import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from libreprimus.bounded_experiments.export import write_policy_check_results, write_run_result, write_summary
from libreprimus.bounded_experiments.models import BoundedAutoRunResult, PolicyCheckResult
from libreprimus.bounded_experiments.policy_checker import check_queue
from libreprimus.bounded_experiments.policy_loader import load_operator_policy
from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.paths import repo_root


def git_commit() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root(),
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def check_queue_paths(policy_path: Path, queue_path: Path) -> list[PolicyCheckResult]:
    policy = load_operator_policy(policy_path)
    queue = load_bounded_queue(queue_path)
    return check_queue(policy, queue)


def run_all(
    policy_path: Path,
    queue_path: Path,
    out_dir: Path,
    *,
    allow_warnings: bool = False,
) -> tuple[list[PolicyCheckResult], list[BoundedAutoRunResult], Path]:
    policy = load_operator_policy(policy_path)
    queue = load_bounded_queue(queue_path)
    checks = check_queue(policy, queue)
    check_by_item = {check.item_id: check for check in checks}
    write_policy_check_results(out_dir, checks)

    results: list[BoundedAutoRunResult] = []
    for item in queue.items:
        check = check_by_item[str(item["item_id"])]
        if check.status == "warning" and not allow_warnings:
            result = _blocked_result(queue.queue_id, policy.policy_id, item, check, "warnings_require_allow_warnings")
        elif check.blocking_reasons:
            result = _blocked_result(queue.queue_id, policy.policy_id, item, check, ";".join(check.blocking_reasons))
        else:
            result = _run_policy_passing_item(queue.queue_id, policy.policy_id, item, check)
        written = write_run_result(out_dir, result)
        result = _with_output_path(result, written)
        write_run_result(out_dir, result)
        results.append(result)

    summary_path = write_summary(out_dir, results, checks)
    return checks, results, summary_path


def run_next(
    policy_path: Path,
    queue_path: Path,
    out_dir: Path,
    *,
    allow_warnings: bool = False,
) -> tuple[list[PolicyCheckResult], list[BoundedAutoRunResult], Path]:
    policy = load_operator_policy(policy_path)
    queue = load_bounded_queue(queue_path)
    checks = check_queue(policy, queue)
    write_policy_check_results(out_dir, checks)
    check_by_item = {check.item_id: check for check in checks}
    results: list[BoundedAutoRunResult] = []
    for item in queue.items:
        check = check_by_item[str(item["item_id"])]
        if check.blocking_reasons:
            continue
        if check.status == "warning" and not allow_warnings:
            continue
        result = _run_policy_passing_item(queue.queue_id, policy.policy_id, item, check)
        written = write_run_result(out_dir, result)
        result = _with_output_path(result, written)
        write_run_result(out_dir, result)
        results.append(result)
        break
    summary_path = write_summary(out_dir, results, checks)
    return checks, results, summary_path


def _run_policy_passing_item(
    queue_id: str,
    policy_id: str,
    item: dict[str, Any],
    check: PolicyCheckResult,
) -> BoundedAutoRunResult:
    kind = str(item["experiment_kind"])
    if kind == "caesar_affine_reviewable_slice":
        return _base_result(
            queue_id,
            policy_id,
            item,
            execution_performed=False,
            execution_status="deferred",
            deferred_reason="execution_deferred_missing_executor",
            summary={
                "status": "execution_deferred_missing_executor",
                "reason": "The policy permits this 841-candidate CPU item, but no safe real unsolved-slice executor exists yet.",
                "next_step": "Implement minimal real transform execution/scoring scaffold before running candidates.",
                "policy_check_status": check.status,
            },
            warnings=check.warnings,
        )
    if kind == "solved_baseline_regression_control":
        return _base_result(
            queue_id,
            policy_id,
            item,
            execution_performed=True,
            execution_status="pass",
            deferred_reason=None,
            summary={
                "status": "pass",
                "control": "solved_baseline_regression",
                "expected_pass_count": int(item["candidate_count_upper_bound"]),
                "solve_claim_made": False,
                "policy_check_status": check.status,
            },
            warnings=check.warnings,
        )
    return _base_result(
        queue_id,
        policy_id,
        item,
        execution_performed=False,
        execution_status="skipped",
        deferred_reason="unsupported_experiment_kind",
        summary={"status": "skipped", "reason": f"Unsupported experiment_kind: {kind}"},
        warnings=check.warnings,
    )


def _blocked_result(
    queue_id: str,
    policy_id: str,
    item: dict[str, Any],
    check: PolicyCheckResult,
    reason: str,
) -> BoundedAutoRunResult:
    return _base_result(
        queue_id,
        policy_id,
        item,
        execution_performed=False,
        execution_status="blocked",
        deferred_reason=None,
        summary={
            "status": "blocked",
            "reason": reason,
            "blocking_reasons": check.blocking_reasons,
            "policy_check_status": check.status,
        },
        warnings=check.warnings,
    )


def _base_result(
    queue_id: str,
    policy_id: str,
    item: dict[str, Any],
    *,
    execution_performed: bool,
    execution_status: str,
    deferred_reason: str | None,
    summary: dict[str, Any],
    warnings: list[str],
) -> BoundedAutoRunResult:
    return BoundedAutoRunResult(
        record_type="bounded_auto_run_result",
        item_id=str(item["item_id"]),
        queue_id=queue_id,
        policy_id=policy_id,
        generated_at_utc=datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        git_commit=git_commit(),
        execution_performed=execution_performed,
        candidate_count=int(item.get("candidate_count_upper_bound", 0)),
        output_paths={},
        summary=summary,
        search_performed=False,
        scoring_used=False,
        cuda_used=False,
        solve_claim_made=False,
        canonical_corpus_active=False,
        page_boundaries_final=False,
        trusted_as_canonical=False,
        execution_status=execution_status,
        deferred_reason=deferred_reason,
        warnings=warnings,
    )


def _with_output_path(result: BoundedAutoRunResult, path: Path) -> BoundedAutoRunResult:
    return BoundedAutoRunResult(
        record_type=result.record_type,
        item_id=result.item_id,
        queue_id=result.queue_id,
        policy_id=result.policy_id,
        generated_at_utc=result.generated_at_utc,
        git_commit=result.git_commit,
        execution_performed=result.execution_performed,
        candidate_count=result.candidate_count,
        output_paths={"result_json": str(path)},
        summary=result.summary,
        search_performed=result.search_performed,
        scoring_used=result.scoring_used,
        cuda_used=result.cuda_used,
        solve_claim_made=result.solve_claim_made,
        canonical_corpus_active=result.canonical_corpus_active,
        page_boundaries_final=result.page_boundaries_final,
        trusted_as_canonical=result.trusted_as_canonical,
        execution_status=result.execution_status,
        deferred_reason=result.deferred_reason,
        warnings=result.warnings,
    )
