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
from libreprimus.bounded_execution.models import MissingReviewableSliceInput
from libreprimus.bounded_execution.mersenne_stream_probe import LEGACY_TARGET_ITEM_ID as STAGE3J_LEGACY_MERSENNE_ITEM_ID
from libreprimus.bounded_execution.mersenne_stream_probe import TARGET_ITEM_ID as STAGE3J_MERSENNE_ITEM_ID
from libreprimus.bounded_execution.mersenne_stream_probe import run_mersenne_stream_probe_item
from libreprimus.bounded_execution.prime_offset_sweep import TARGET_ITEM_ID as STAGE3G_PRIME_OFFSET_ITEM_ID
from libreprimus.bounded_execution.prime_offset_sweep import run_prime_offset_sweep_item
from libreprimus.bounded_execution.reset_advance_ablation import TARGET_ITEM_ID as STAGE3H_RESET_ADVANCE_ITEM_ID
from libreprimus.bounded_execution.reset_advance_ablation import run_reset_advance_ablation_item
from libreprimus.bounded_execution.runner import run_caesar_affine_item
from libreprimus.bounded_execution.vigenere_key_pack import HISTORICAL_ITEM_ID as STAGE3I_HISTORY_KEY_PACK_ITEM_ID
from libreprimus.bounded_execution.vigenere_key_pack import TARGET_ITEM_ID as STAGE3F_KEY_PACK_ITEM_ID
from libreprimus.bounded_execution.vigenere_key_pack import run_vigenere_key_pack_item
from libreprimus.bounded_execution.vigenere_key_list import run_vigenere_key_list_item
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
            result = _run_policy_passing_item(queue.queue_id, policy.policy_id, item, check, out_dir=out_dir)
        written = write_run_result(out_dir, result)
        result = _with_output_path(result, written)
        write_run_result(out_dir, result)
        results.append(result)

    summary_path = write_summary(out_dir, results, checks, filename=_summary_filename(out_dir))
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
        result = _run_policy_passing_item(queue.queue_id, policy.policy_id, item, check, out_dir=out_dir)
        written = write_run_result(out_dir, result)
        result = _with_output_path(result, written)
        write_run_result(out_dir, result)
        results.append(result)
        break
    summary_path = write_summary(out_dir, results, checks, filename=_summary_filename(out_dir))
    return checks, results, summary_path


def _run_policy_passing_item(
    queue_id: str,
    policy_id: str,
    item: dict[str, Any],
    check: PolicyCheckResult,
    *,
    out_dir: Path,
) -> BoundedAutoRunResult:
    kind = str(item["experiment_kind"])
    if kind == "caesar_affine_reviewable_slice":
        try:
            stage3a_summary = run_caesar_affine_item(
                item,
                out_dir=out_dir / str(item["item_id"]),
                top_k=25,
                policy_id=policy_id,
            )
        except MissingReviewableSliceInput as error:
            return _base_result(
                queue_id,
                policy_id,
                item,
                execution_performed=False,
                execution_status="deferred",
                deferred_reason="missing_reviewable_slice_input",
                summary={
                    "status": "missing_reviewable_slice_input",
                    "reason": str(error),
                    "next_step": "Add a precise safe selector or regenerate ignored corpus-candidate metadata.",
                    "policy_check_status": check.status,
                },
                warnings=check.warnings,
            )
        return _base_result(
            queue_id,
            policy_id,
            item,
            execution_performed=True,
            execution_status="pass",
            deferred_reason=None,
            summary={
                "status": "pass",
                "stage3a_run_id": stage3a_summary.run_id,
                "input_slice_id": stage3a_summary.input_slice_id,
                "input_length": stage3a_summary.input_length,
                "candidate_count": stage3a_summary.candidate_count,
                "caesar_candidate_count": stage3a_summary.caesar_candidate_count,
                "affine_candidate_count": stage3a_summary.affine_candidate_count,
                "top_candidate": stage3a_summary.top_candidate,
                "candidate_output_paths": stage3a_summary.output_paths,
                "solve_claim_made": False,
                "policy_check_status": check.status,
            },
            search_performed=stage3a_summary.search_performed,
            scoring_used=stage3a_summary.scoring_used,
            output_paths=dict(stage3a_summary.output_paths),
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
    if kind == "vigenere_tiny_key_list_preview":
        stage3d_summary = run_vigenere_key_list_item(
            item,
            out_dir=out_dir / str(item["item_id"]),
            top_k=int(item.get("candidate_count_upper_bound", 4)),
            policy_id=policy_id,
        )
        return _base_result(
            queue_id,
            policy_id,
            item,
            execution_performed=True,
            execution_status="pass",
            deferred_reason=None,
            summary={
                "status": "pass",
                "stage3d_run_id": stage3d_summary.run_id,
                "input_slice_id": stage3d_summary.input_slice_id,
                "input_length": stage3d_summary.input_length,
                "candidate_count": stage3d_summary.candidate_count,
                "vigenere_candidate_count": stage3d_summary.vigenere_candidate_count,
                "top_candidate": stage3d_summary.top_candidate,
                "candidate_output_paths": stage3d_summary.output_paths,
                "solve_claim_made": False,
                "policy_check_status": check.status,
            },
            search_performed=stage3d_summary.search_performed,
            scoring_used=stage3d_summary.scoring_used,
            output_paths=dict(stage3d_summary.output_paths),
            warnings=check.warnings,
        )
    if kind == "vigenere_key_pack" and item.get("item_id") in {
        STAGE3F_KEY_PACK_ITEM_ID,
        STAGE3I_HISTORY_KEY_PACK_ITEM_ID,
    }:
        key_pack_summary = run_vigenere_key_pack_item(
            item,
            out_dir=out_dir / str(item["item_id"]),
            top_k=25,
            policy_id=policy_id,
        )
        return _base_result(
            queue_id,
            policy_id,
            item,
            execution_performed=True,
            execution_status="pass",
            deferred_reason=None,
            summary={
                "status": "pass",
                "vigenere_key_pack_run_id": key_pack_summary.run_id,
                "input_slice_id": key_pack_summary.input_slice_id,
                "input_length": key_pack_summary.input_length,
                "expected_candidate_count": key_pack_summary.expected_candidate_count,
                "executed_candidate_count": key_pack_summary.executed_candidate_count,
                "deferred_candidate_count": key_pack_summary.deferred_candidate_count,
                "candidate_count": key_pack_summary.candidate_count,
                "vigenere_candidate_count": key_pack_summary.vigenere_candidate_count,
                "top_candidate": key_pack_summary.top_candidate,
                "candidate_output_paths": key_pack_summary.output_paths,
                "confidence_distribution": key_pack_summary.confidence_distribution,
                "solve_claim_made": False,
                "policy_check_status": check.status,
            },
            search_performed=key_pack_summary.search_performed,
            scoring_used=key_pack_summary.scoring_used,
            output_paths=dict(key_pack_summary.output_paths),
            warnings=check.warnings + key_pack_summary.warnings,
        )
    if kind == "prime_minus_one_offset_sweep" and item.get("item_id") == STAGE3G_PRIME_OFFSET_ITEM_ID:
        stage3g_summary = run_prime_offset_sweep_item(
            item,
            out_dir=out_dir / str(item["item_id"]),
            top_k=25,
            policy_id=policy_id,
        )
        return _base_result(
            queue_id,
            policy_id,
            item,
            execution_performed=True,
            execution_status="pass",
            deferred_reason=None,
            summary={
                "status": "pass",
                "stage3g_run_id": stage3g_summary.run_id,
                "input_slice_id": stage3g_summary.input_slice_id,
                "input_length": stage3g_summary.input_length,
                "expected_candidate_count": stage3g_summary.expected_candidate_count,
                "executed_candidate_count": stage3g_summary.executed_candidate_count,
                "deferred_candidate_count": stage3g_summary.deferred_candidate_count,
                "candidate_count": stage3g_summary.candidate_count,
                "prime_candidate_count": stage3g_summary.prime_candidate_count,
                "top_candidate": stage3g_summary.top_candidate,
                "candidate_output_paths": stage3g_summary.output_paths,
                "confidence_distribution": stage3g_summary.confidence_distribution,
                "solve_claim_made": False,
                "policy_check_status": check.status,
            },
            search_performed=stage3g_summary.search_performed,
            scoring_used=stage3g_summary.scoring_used,
            output_paths=dict(stage3g_summary.output_paths),
            warnings=check.warnings + stage3g_summary.warnings,
        )
    if kind == "reset_advance_ablation" and item.get("item_id") == STAGE3H_RESET_ADVANCE_ITEM_ID:
        stage3h_summary = run_reset_advance_ablation_item(
            item,
            out_dir=out_dir / str(item["item_id"]),
            top_k=25,
            policy_id=policy_id,
        )
        return _base_result(
            queue_id,
            policy_id,
            item,
            execution_performed=True,
            execution_status="pass",
            deferred_reason=None,
            summary={
                "status": "pass",
                "stage3h_run_id": stage3h_summary.run_id,
                "input_slice_id": stage3h_summary.input_slice_id,
                "input_length": stage3h_summary.input_length,
                "expected_candidate_count": stage3h_summary.expected_candidate_count,
                "executed_candidate_count": stage3h_summary.executed_candidate_count,
                "deferred_candidate_count": stage3h_summary.deferred_candidate_count,
                "negative_control_count": stage3h_summary.negative_control_count,
                "candidate_count": stage3h_summary.candidate_count,
                "reset_advance_candidate_count": stage3h_summary.reset_advance_candidate_count,
                "top_candidate": stage3h_summary.top_candidate,
                "candidate_output_paths": stage3h_summary.output_paths,
                "confidence_distribution": stage3h_summary.confidence_distribution,
                "solve_claim_made": False,
                "policy_check_status": check.status,
            },
            search_performed=stage3h_summary.search_performed,
            scoring_used=stage3h_summary.scoring_used,
            output_paths=dict(stage3h_summary.output_paths),
            warnings=check.warnings + stage3h_summary.warnings,
        )
    if kind == "mersenne_prime_stream_tiny" and item.get("item_id") in {
        STAGE3J_LEGACY_MERSENNE_ITEM_ID,
        STAGE3J_MERSENNE_ITEM_ID,
    }:
        stage3j_summary = run_mersenne_stream_probe_item(
            item,
            out_dir=out_dir / str(item["item_id"]),
            top_k=25,
            policy_id=policy_id,
        )
        return _base_result(
            queue_id,
            policy_id,
            item,
            execution_performed=True,
            execution_status="pass",
            deferred_reason=None,
            summary={
                "status": "pass",
                "stage3j_run_id": stage3j_summary.run_id,
                "input_slice_id": stage3j_summary.input_slice_id,
                "input_length": stage3j_summary.input_length,
                "expected_candidate_count": stage3j_summary.expected_candidate_count,
                "executed_candidate_count": stage3j_summary.executed_candidate_count,
                "deferred_candidate_count": stage3j_summary.deferred_candidate_count,
                "candidate_count": stage3j_summary.candidate_count,
                "mersenne_candidate_count": stage3j_summary.mersenne_candidate_count,
                "top_candidate": stage3j_summary.top_candidate,
                "candidate_output_paths": stage3j_summary.output_paths,
                "unique_stream_signature_count": stage3j_summary.unique_stream_signature_count,
                "duplicate_stream_signature_count": stage3j_summary.duplicate_stream_signature_count,
                "confidence_distribution": stage3j_summary.confidence_distribution,
                "solve_claim_made": False,
                "policy_check_status": check.status,
            },
            search_performed=stage3j_summary.search_performed,
            scoring_used=stage3j_summary.scoring_used,
            output_paths=dict(stage3j_summary.output_paths),
            warnings=check.warnings + stage3j_summary.warnings,
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
    search_performed: bool = False,
    scoring_used: bool = False,
    output_paths: dict[str, str] | None = None,
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
        output_paths=output_paths or {},
        summary=summary,
        search_performed=search_performed,
        scoring_used=scoring_used,
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
    output_paths = dict(result.output_paths)
    output_paths["result_json"] = str(path)
    return BoundedAutoRunResult(
        record_type=result.record_type,
        item_id=result.item_id,
        queue_id=result.queue_id,
        policy_id=result.policy_id,
        generated_at_utc=result.generated_at_utc,
        git_commit=result.git_commit,
        execution_performed=result.execution_performed,
        candidate_count=result.candidate_count,
        output_paths=output_paths,
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


def _summary_filename(out_dir: Path) -> str:
    return "bounded-auto-run-summary.json" if out_dir.name == "stage3a" else "summary.json"
